'''
Integration tests for remote.
'''
import os
import tempfile
from boss.core import remote, fs


def test_put(server):
    ''' Test put() transfers file to the remote end. '''
    for uid in server.users:
        target_dir = tempfile.mkdtemp()
        source_file = os.path.join(target_dir, 'foo_src')
        target_file = os.path.join(target_dir, 'foo_dest')

        fs.write(source_file, 'Test')
        assert not fs.exists(target_file)

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.put(
                sftp,
                local_path=source_file,
                remote_path=target_file,
                confirm=True
            )
            assert fs.read(target_file) == 'Test'
