'''
A core utility module to deal with remote host and operations
over SSH connection.
Uses paramiko directly for remote execution and transfers.
'''


def put(sftp_client, **params):
    '''
    Transfers a local file to the remote path via SFTP.
    '''

    local_path = params['local_path']
    remote_path = params['remote_path']
    callback = params.get('callback')
    confirm = params.get('confirm')

    # Do the put operation.
    return sftp_client.put(local_path, remote_path, callback, confirm)
