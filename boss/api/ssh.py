''' SSH module based on paramiko. '''

import os
from time import time
from tempfile import mkdtemp
from stat import S_ISDIR

from boss import state
from boss.core import remote
from boss.core.fs import compress
from boss.core.util.types import is_string, is_iterable


def run(command, **params):
    '''
    Execute a command or a list of commands on the remote host over SSH.
    '''

    # Keyword args
    raw = params.get('raw') or False
    return_output = params.get('return_output') or True

    # If command is a list of commands,
    # concat the commands and run them all.
    if not is_string(command) and is_iterable(command):
        command = '; '.join(command)

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


def normalize_path(remote_path):
    '''
    Normalize remote path.
    Expand home directory '~' in the path if it exists.
    '''
    home = resolve_cwd()

    # Expand home directory markers (tildes, etc)
    if remote_path.startswith('~'):
        remote_path = remote_path.replace('~', home)

    return remote_path


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
    sftp = resolve_client().open_sftp()
    sftp_connections.update({host_string: sftp})

    return sftp


def resolve_cwd():
    '''
    Resolve current working directory of the remote host.

    TODO: After refactor resolve cwd at the very begining,
    instead of every time before any operation.
    '''
    remote_state = state.get('remote')
    host_string = state.get('env').host_string

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
    remote_path = normalize_path(remote_path)

    # If remote_path is a directory, upload it with the same filename.
    if is_dir(remote_path):
        filename = os.path.basename(local_path)
        remote_path = os.path.join(remote_path, filename)

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
    remote_path = normalize_path(remote_path)

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
    remote_path = normalize_path(remote_path)

    return remote.read(sftp, remote_path, callback)


def write(remote_path, data, **params):
    '''
    Write data to a remote file on the remote host.
    '''
    sftp = resolve_sftp_client()
    remote_path = normalize_path(remote_path)

    return remote.write(
        sftp,
        remote_path,
        data=data,
        file_size=params.get('file_size'),
        callback=params.get('callback'),
        confirm=params.get('confirm')
    )


def upload_files(files, remote_path):
    ''' Upload multiple files. '''
    for filename in files:
        put(filename, remote_path)


def upload_dir(local_path, remote_path, callback=None):
    ''' Upload local directory to the remote. '''
    tmp_folder = mkdtemp()
    tar_filename = os.path.basename(local_path) + '.tar.gz'
    tar_path = os.path.join(tmp_folder, tar_filename)
    remote_path = normalize_path(remote_path)

    # Compress the directory.
    compress(local_path, tar_path)

    # Upload the tar zipped file to the remote.
    # The compressed folder gets uploaded to a temp path first.
    # Then later is extracted to the provided path on the remote.
    remote_tmp_path = '/tmp/upload-' + str(time()).replace('.', '-')
    put(tar_path, remote_tmp_path, callback)
    # Extract the files to the remote directory
    run('mkdir -p {}'.format(remote_path))
    run(
        'tar zxvf {src} --strip-components=1 -C {dest}'.format(
            src=remote_tmp_path,
            dest=remote_path
        )
    )
    run('rm -rf {}'.format(remote_tmp_path))

    os.remove(tar_path)


def stat(remote_path):
    '''
    Retrieve information about a file on the remote system.
    '''
    sftp = resolve_sftp_client()

    return remote.stat(sftp, remote_path)


def exists(path):
    '''
    Check if the remote path exists.
    '''
    try:
        path = normalize_path(path)
        stat(path)
        return True
    except IOError:
        return False


def is_dir(path):
    '''
    Check if the remote path a directory.
    TODO: Move this to a remote fs module.
    '''
    try:
        path = normalize_path(path)
        mode = stat(path).st_mode

        return S_ISDIR(mode)
    except IOError:
        return False
