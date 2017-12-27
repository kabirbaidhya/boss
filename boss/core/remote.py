'''
A core utility module to deal with remote host and operations
over SSH connection.

This is an abstraction over the underlying SSH/SFTP transport
which uses paramiko directly for remote execution and transfers.
'''

import os
from StringIO import StringIO

from boss.core.util.object import with_only


def normalize_path(sftp_client, remote_path):
    home = sftp_client.normalize('.')

    # Expand home directory markers (tildes, etc)
    if remote_path.startswith('~'):
        remote_path = os.path.join(home, remote_path.replace('~', ''))

    return remote_path


def put(sftp_client, **params):
    '''
    Transfers (upload) a local file to the remote path via SFTP.
    '''

    local_path = params['local_path']
    remote_path = normalize_path(sftp_client, params['remote_path'])
    callback = params.get('callback')
    confirm = params.get('confirm')

    return sftp_client.put(local_path, remote_path, callback, confirm)


def get(sftp_client, **params):
    '''
    Transfers (download) a remote file to the local path via SFTP.
    '''

    remote_path = normalize_path(sftp_client, params['remote_path'])
    local_path = params['local_path']
    callback = params.get('callback')

    return sftp_client.get(remote_path, local_path, callback)


def run(client, command, **params):
    '''
    Execute a command on a opened instance
    of SSHClient for a remote host.
    '''

    # Pass only the parameters known to exec_command function.
    known_params = with_only(params, [
        'bufsize',
        'timeout',
        'get_pty',
        'environment'
    ])

    # Execute the command.
    return client.exec_command(command, **known_params)


def read(client, remote_path, callback=None):
    '''
    Read a remote file given by the path on the remote host
    and return it's contents as string.
    '''
    fd = StringIO()
    client.getfo(remote_path, fd, callback)

    return fd.getvalue()


def write(client, remote_path, **params):
    '''
    Write data to a remote file on the remote host.
    '''
    data = params['data']
    file_size = params.get('file_size')
    callback = params.get('callback')
    confirm = params.get('confirm')

    fd = StringIO(data)

    return client.putfo(fd, remote_path, file_size, callback, confirm)
