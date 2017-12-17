'''
A core utility module to deal with remote host and operations
over SSH connection.

This is an abstraction over the underlying SSH/SFTP transport
which uses paramiko directly for remote execution and transfers.
'''


def put(sftp_client, **params):
    '''
    Transfers (upload) a local file to the remote path via SFTP.
    '''

    local_path = params['local_path']
    remote_path = params['remote_path']
    callback = params.get('callback')
    confirm = params.get('confirm')

    return sftp_client.put(local_path, remote_path, callback, confirm)


def get(sftp_client, **params):
    '''
    Transfers (download) a remote file to the local path via SFTP.
    '''

    remote_path = params['remote_path']
    local_path = params['local_path']
    callback = params.get('callback')

    return sftp_client.get(remote_path, local_path, callback)
