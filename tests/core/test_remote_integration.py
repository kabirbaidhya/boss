'''
Integration tests for remote.
TODO: Replace mock-ssh-server with some other alternatives.
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

        fs.write(source_file, 'Test put operation')
        assert not fs.exists(target_file)

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.put(
                sftp,
                local_path=source_file,
                remote_path=target_file,
                confirm=True
            )
            assert fs.read(target_file) == 'Test put operation'


def test_get(server):
    ''' Test get() transfers remote file to the local. '''
    for uid in server.users:
        target_dir = tempfile.mkdtemp()
        source_file = os.path.join(target_dir, 'foo_src')
        target_file = os.path.join(target_dir, 'foo_dest')

        fs.write(source_file, 'Test get operation')
        assert not fs.exists(target_file)

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.get(
                sftp,
                remote_path=source_file,
                local_path=target_file
            )
            assert fs.read(target_file) == 'Test get operation'


def test_run(server):
    ''' Test run() executes a command over ssh. '''
    for uid in server.users:
        with server.client(uid) as client:
            (_, stdout, _) = remote.run(client, 'python --version')

            assert stdout.read() is not None
