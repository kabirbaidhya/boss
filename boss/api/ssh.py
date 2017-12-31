''' SSH module based on paramiko. '''

from boss import state
from boss.core import remote


def run(command, **params):
    '''
    Execute a command on the remote host over SSH.
    '''

    # Keyword args
    raw = params.get('raw') or False
    return_output = params.get('return_output') or True

    # Execute the command and get the IO streams.
    (stdin, stdout, stderr) = remote.run(resolve_client(), command, **params)

    # Return the raw result if raw=True.
    if raw:
        return (stdin, stdout, stderr)

    # If output is required (usually),
    # return a list of each output line.
    if return_output:
        lines = []

        for l in stdout:
            lines.append(l.strip())

        return lines

    # For return_output=False,
    # just walk until the end of the stream
    # and just return without any output.
    for _ in stdout:
        pass


def resolve_client():
    '''
    Resolves already opened SSHClient connection.
    '''
    host_string = state.get('env').host_string
    client = state.get('connections')[host_string]

    return client


def resolve_sftp_client():
    '''
    Resolves (opens or gets already opened) sftp connection.
    '''
    host_string = state.get('env').host_string
    sftp_connections = state.get('sftp_connections')

    # If already opened sftp connection found in the state, return it.
    if sftp_connections.has_key(host_string):
        return sftp_connections[host_string]

    # Open a new SFTP connection and put in on the state.
    ssh_client = state.get('connections')[host_string]
    sftp = ssh_client.open_sftp()
    sftp_connections.update({host_string: sftp})

    return sftp


def resolve_cwd(host_string):
    '''
    Resolve current working directory of the remote host.

    TODO: After refactor resolve cwd at the very begining,
    instead of every time before any operation.
    '''
    remote_state = state.get('remote')

    if not remote_state.get(host_string):
        remote_state[host_string] = {}

    remote_host_state = remote_state.get(host_string)

    if not remote_host_state.get('cwd'):
        cwd = remote.cwd(resolve_client())
        remote_host_state['cwd'] = cwd

        return cwd

    return remote_host_state.get('cwd')


def put(local_path, remote_path, callback=None):
    '''
    Transfers a local file to the remote path via SFTP (Paramiko).
    '''
    sftp = resolve_sftp_client()

    # Do the put operation.
    return remote.put(
        sftp,
        local_path=local_path,
        remote_path=remote_path,
        callback=callback
    )


def get(local_path, remote_path, callback=None):
    '''
    Transfers a remote file to local path via SFTP (Paramiko).
    '''
    sftp = resolve_sftp_client()

    # Do the get operation.
    return remote.get(
        sftp,
        remote_path=remote_path,
        local_path=local_path,
        callback=callback
    )


def read(remote_path, callback=None):
    '''
    Read a remote file given by the path on the remote host
    and return it's contents as string.
    '''
    sftp = resolve_sftp_client()

    return remote.read(sftp, remote_path, callback)


def write(remote_path, data, **params):
    '''
    Write data to a remote file on the remote host.
    '''
    sftp = resolve_sftp_client()

    return remote.write(
        sftp,
        remote_path,
        data=data,
        file_size=params.get('file_size'),
        callback=params.get('callback'),
        confirm=params.get('confirm')
    )
