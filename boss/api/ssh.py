''' SSH module based on paramiko. '''


def put(client, **params):
    '''
    Transfers a local file to the remote path via SFTP (Paramiko).
    '''

    local_path = params['local_path']
    remote_path = params['remote_path']
    callback = params.get('remote_path')

    # Open a SFTP connection.
    sftp = client.open_sftp()

    # Do the put operation.
    return sftp.put(local_path, remote_path, callback)
