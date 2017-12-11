''' SSH module based on paramiko. '''
from fabric.state import connections, env


def put(local_path, remote_path, callback=None):
    '''
    Copies a local file to the remote path via SFTP (Paramiko).
    '''
    # Open a SFTP connection.
    ftp = connections[env.host_string].open_sftp()

    return ftp.put(local_path, remote_path, callback)
