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


# def test_put_with_home_path(server):
#     ''' Test put() transfers file to the remote end. '''
#     for uid in server.users:
#         target_dir = tempfile.mkdtemp()
#         source_file = os.path.join(target_dir, 'foo_src')
#         remote_file = '~/test-remote-path/file'

#         fs.write(source_file, 'Test put operation')
#         assert not fs.exists(remote_file)

#         with server.client(uid) as client:
#             sftp = client.open_sftp()
#             remote.put(
#                 sftp,
#                 local_path=source_file,
#                 remote_path=remote_file,
#                 confirm=True
#             )
#             assert fs.read('/test-remote-path/file') == 'Test put operation'


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


def test_normalize_path(server):
    ''' Test normalize_path() returns the path as it is. '''
    for uid in server.users:
        with server.client(uid) as client:
            sftp = client.open_sftp()
            result = remote.normalize_path(sftp, '/just/test')
            assert result == '/just/test'


def test_normalize_path_expands_home_path(server):
    ''' Test normalize_path() expands the home path if (~) is found. '''
    for uid in server.users:
        with server.client(uid) as client:
            sftp = client.open_sftp()
            result = remote.normalize_path(sftp, '~/just/test')
            assert result == '/just/test'
