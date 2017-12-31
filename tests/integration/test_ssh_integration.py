''' Integration tests for ssh module. '''


import os
from tempfile import mkdtemp
from mock import patch

from boss.core import fs
from boss.api import ssh


def test_upload_dir(server):
    ''' Test upload_dir() transfers a local directory to the remote end. '''

    # Setup local directory.
    local_dir = os.path.join(mkdtemp(), 'test')

    os.mkdir(local_dir)
    os.mkdir(os.path.join(local_dir, 'a'))
    os.mkdir(os.path.join(local_dir, 'b'))

    fs.write(os.path.join(local_dir, 'a/foo.txt'), 'Foo')
    fs.write(os.path.join(local_dir, 'b/bar.txt'), 'Bar')

    for uid in server.users:
        remote_path = os.path.join(server.ROOT_DIR, 'remote')

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client

                assert not fs.exists(remote_path)

                # Upload the directory
                ssh.upload_dir(local_dir, remote_path)

                # Test the whole directory got uploaded with all files
                assert fs.exists(remote_path)
                assert fs.exists(os.path.join(remote_path, 'a'))
                assert fs.exists(os.path.join(remote_path, 'b'))
                assert fs.read(os.path.join(remote_path, 'a/foo.txt')) == 'Foo'
                assert fs.read(os.path.join(remote_path, 'b/bar.txt')) == 'Bar'


def test_upload_dir_with_home_directory(server):
    '''
    Test upload_dir() transfers a local directory to the remote end,
    when remote_path includes home directory `~`.
    '''

    # Setup local directory.
    local_dir = os.path.join(mkdtemp(), 'test2')

    os.mkdir(local_dir)
    os.mkdir(os.path.join(local_dir, 'a'))
    os.mkdir(os.path.join(local_dir, 'b'))

    fs.write(os.path.join(local_dir, 'a/foo.txt'), 'Foo')
    fs.write(os.path.join(local_dir, 'b/bar.txt'), 'Bar')

    for uid in server.users:
        remote_path = '~/deployment'

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client
                with patch('boss.api.ssh.resolve_cwd') as rcwd_m:
                    rcwd_m.return_value = server.ROOT_DIR

                    expanded_remote_path = os.path.join(
                        server.ROOT_DIR, 'deployment')

                    assert not fs.exists(expanded_remote_path)

                    # Upload the directory
                    ssh.upload_dir(local_dir, remote_path)

                    # Test the whole directory got uploaded with all files
                    assert fs.exists(expanded_remote_path)
                    assert fs.exists(os.path.join(expanded_remote_path, 'a'))
                    assert fs.exists(os.path.join(expanded_remote_path, 'b'))
                    assert fs.read(os.path.join(
                        expanded_remote_path, 'a/foo.txt')) == 'Foo'
                    assert fs.read(os.path.join(
                        expanded_remote_path, 'b/bar.txt')) == 'Bar'


def test_put_when_remote_directory_provided(server):
    '''
    If remote directory path is provided instead of remote filename,
    put() should upload the local file to the remote directory with the same filename.
    '''
    for uid in server.users:
        source_file = os.path.join(server.ROOT_DIR, 'abc.txt')
        target_directory = os.path.join(server.ROOT_DIR, 'remote-directory')
        expected_target_file = os.path.join(target_directory, 'abc.txt')
        os.mkdir(target_directory)

        fs.write(source_file, 'Test put operation')

        assert fs.exists(target_directory)
        assert not fs.exists(expected_target_file)

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client
                ssh.put(
                    local_path=source_file,
                    remote_path=target_directory
                )

                assert fs.exists(expected_target_file)
                assert fs.read(expected_target_file) == 'Test put operation'
