'''
A core utility module to deal with remote host and operations
over SSH connection.

This is an abstraction over the underlying SSH/SFTP transport
which uses paramiko directly for remote execution and transfers.
'''

import os


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
    bufsize = params.get('bufsize')
    timeout = params.get('timeout')
    environment = params.get('env')

    # Execute the command.
    return client.exec_command(
        command,
        bufsize=bufsize,
        timeout=timeout,
        environment=environment
    )
