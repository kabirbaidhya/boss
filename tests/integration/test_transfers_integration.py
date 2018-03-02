''' Integration tests for boss.api.transfers module. '''
import os
from tempfile import mkdtemp
from mock import patch

from boss.core import fs
from boss.api.transfers import upload, upload_dir, BulkUploader


def test_upload(server, capsys):
    '''
    Test upload() uploads the local file to the remote directory.
    '''
    for uid in server.users:
        local_file = os.path.join(server.ROOT_DIR, 'abc.txt')
        target_directory = os.path.join(server.ROOT_DIR, 'remote-directory')
        remote_path = os.path.join(server.ROOT_DIR, 'remote-directory/abc.txt')

        os.mkdir(target_directory)

        fs.write(local_file, 'Test put operation')

        assert not fs.exists(remote_path)

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client

                upload(local_file, remote_path)

                capsys.readouterr()

                assert fs.exists(remote_path)
                assert fs.read(remote_path) == 'Test put operation'


def test_upload_when_remote_directory_provided(server, capsys):
    '''
    If remote directory path is provided instead of remote filename,
    upload() should upload the local file to the remote directory with the same filename.
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

                upload(source_file, target_directory)

                capsys.readouterr()

                assert fs.exists(expected_target_file)
                assert fs.read(expected_target_file) == 'Test put operation'


def test_upload_dir(server, capsys):
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
                upload_dir(local_dir, remote_path)

                capsys.readouterr()

                # Test the whole directory got uploaded with all files
                assert fs.exists(remote_path)
                assert fs.exists(os.path.join(remote_path, 'a'))
                assert fs.exists(os.path.join(remote_path, 'b'))
                assert fs.read(os.path.join(remote_path, 'a/foo.txt')) == 'Foo'
                assert fs.read(os.path.join(remote_path, 'b/bar.txt')) == 'Bar'


def test_upload_dir_with_home_directory(server, capsys):
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
                    upload_dir(local_dir, remote_path)

                    capsys.readouterr()

                    # Test the whole directory got uploaded with all files
                    assert fs.exists(expanded_remote_path)
                    assert fs.exists(os.path.join(expanded_remote_path, 'a'))
                    assert fs.exists(os.path.join(expanded_remote_path, 'b'))
                    assert fs.read(os.path.join(
                        expanded_remote_path, 'a/foo.txt')) == 'Foo'
                    assert fs.read(os.path.join(
                        expanded_remote_path, 'b/bar.txt')) == 'Bar'


def test_bulk_uploads(server, capsys):
    '''
    Test upload_dir() transfers a local directory to the remote end,
    when remote_path includes home directory `~`.
    '''

    # Setup local directory.
    local_dir1 = os.path.join(mkdtemp(), 'test2')
    local_dir2 = mkdtemp()

    os.mkdir(local_dir1)
    os.mkdir(os.path.join(local_dir1, 'a'))
    os.mkdir(os.path.join(local_dir1, 'b'))

    fs.write(os.path.join(local_dir1, 'a/foo.txt'), 'Foo')
    fs.write(os.path.join(local_dir1, 'b/bar.txt'), 'Bar')
    fs.write(os.path.join(local_dir2, 'helloworld.txt'), 'Hello World')

    for uid in server.users:
        remote_path1 = os.path.join(server.ROOT_DIR, 'test3')
        remote_path2 = os.path.join(server.ROOT_DIR, 'helloworld.txt')

        assert not fs.exists(remote_path1)
        assert not fs.exists(remote_path2)

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client

                uploader = BulkUploader()
                uploader.add(local_dir1, remote_path1)
                uploader.add(
                    os.path.join(local_dir2, 'helloworld.txt'),
                    remote_path2
                )

                # Upload the directory
                uploader.upload()

                capsys.readouterr()

                assert fs.exists(remote_path1)
                assert fs.exists(remote_path2)

                assert fs.read(os.path.join(
                    remote_path1, 'a/foo.txt')) == 'Foo'
                assert fs.read(os.path.join(
                    remote_path1, 'b/bar.txt')) == 'Bar'
                assert fs.read(remote_path2) == 'Hello World'


def test_bulk_uploads_with_unexisting_remote_paths(server, capsys):
    '''
    Test bulk uploads transfers a local directory to the remote end,
    when there are the remote paths do not exist.
    '''

    # Setup local directory.
    local_path = mkdtemp()

    local_file1 = os.path.join(local_path, 'foo.txt')
    local_file2 = os.path.join(local_path, 'bar.txt')
    local_file3 = os.path.join(local_path, 'baz.txt')
    local_file4 = os.path.join(local_path, 'hello.txt')
    local_file5 = os.path.join(local_path, 'world.txt')

    fs.write(local_file1, 'Foo')
    fs.write(local_file2, 'Bar')
    fs.write(local_file3, 'Baz')
    fs.write(local_file4, 'Hello')
    fs.write(local_file5, 'World')

    for uid in server.users:
        remote_path1 = os.path.join(server.ROOT_DIR, 's0/foo.txt')
        remote_path2 = os.path.join(server.ROOT_DIR, 's0/s1/bar.txt')
        remote_path3 = os.path.join(server.ROOT_DIR, 's0/s1/s2/baz.txt')
        remote_path4 = os.path.join(
            server.ROOT_DIR, 's1/s0/s2/s3/s4/hello.txt')
        remote_path5 = os.path.join(server.ROOT_DIR, 's0/s1/s2/s3/world.txt')

        assert not fs.exists(remote_path1)
        assert not fs.exists(remote_path2)
        assert not fs.exists(remote_path3)
        assert not fs.exists(remote_path4)
        assert not fs.exists(remote_path5)

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client

                uploader = BulkUploader()
                uploader.add(local_file1, remote_path1)
                uploader.add(local_file2, remote_path2)
                uploader.add(local_file3, remote_path3)
                uploader.add(local_file4, remote_path4)
                uploader.add(local_file5, remote_path5)

                # Upload the directory
                uploader.upload()

                capsys.readouterr()

                assert fs.exists(remote_path1)
                assert fs.exists(remote_path2)
                assert fs.exists(remote_path3)
                assert fs.exists(remote_path4)
                assert fs.exists(remote_path5)

                assert fs.read(remote_path1) == 'Foo'
                assert fs.read(remote_path2) == 'Bar'
                assert fs.read(remote_path3) == 'Baz'
                assert fs.read(remote_path4) == 'Hello'
                assert fs.read(remote_path5) == 'World'


def test_bulk_uploads_supports_different_remote_filenames(server, capsys):
    '''
    Test bulk uploads supports transfering files with different
    filenames on the remote host.
    '''

    # Setup local directory.
    local_path = mkdtemp()

    local_file1 = os.path.join(local_path, 'foo.txt')
    local_file2 = os.path.join(local_path, 'bar.txt')

    fs.write(local_file1, 'Foo')
    fs.write(local_file2, 'Bar')

    for uid in server.users:
        remote_path1 = os.path.join(server.ROOT_DIR, 's0/test1.txt')
        remote_path2 = os.path.join(server.ROOT_DIR, 's0/s1/test2.txt')

        assert not fs.exists(remote_path1)
        assert not fs.exists(remote_path2)

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client

                uploader = BulkUploader()
                uploader.add(local_file1, remote_path1)
                uploader.add(local_file2, remote_path2)

                # Upload the directory
                uploader.upload()

                capsys.readouterr()

                assert fs.exists(remote_path1)
                assert fs.exists(remote_path2)

                assert fs.read(remote_path1) == 'Foo'
                assert fs.read(remote_path2) == 'Bar'
