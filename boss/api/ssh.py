''' SSH module based on paramiko. '''

from boss import state
from boss.core import remote


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
    sftp = state.get('connections')[host_string].open_sftp()
    sftp_connections.update({host_string: sftp})

    return sftp


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
