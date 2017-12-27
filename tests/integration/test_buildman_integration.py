'''
Integration tests for buildman.
TODO: Replace mock-ssh-server with some other alternatives.
'''

import os
from mock import patch
from boss.core import fs
from boss.api.deployment import buildman

REMOTE_ENV_FILE = '''
FOO=bar
GREETING=Hello World
'''


def test_load_history(server):
    ''' Test load_history() works. '''
    for uid in server.users:
        path = os.path.join(server.ROOT_DIR, 'testfile.json')
        fs.write(path, '{"foo": "bar", "hello": "world"}')

        with server.client(uid) as client:
            with patch('boss.api.deployment.buildman.get_builds_file') as gbf_m:
                gbf_m.return_value = path

                with patch('boss.api.ssh.resolve_sftp_client') as rsc_m:
                    rsc_m.return_value = client.open_sftp()
                    result = buildman.load_history()

                    assert result['foo'] == 'bar'
                    assert result['hello'] == 'world'


def test_save_history(server):
    ''' Test save_history() works. '''

    for uid in server.users:
        path = os.path.join(server.ROOT_DIR, 'history.json')

        assert not fs.exists(path)

        with server.client(uid) as client:
            with patch('boss.api.deployment.buildman.get_builds_file') as gbf_m:
                gbf_m.return_value = path

                with patch('boss.api.ssh.resolve_sftp_client') as rsc_m:
                    rsc_m.return_value = client.open_sftp()
                    buildman.save_history({
                        'foo': 'bar',
                        'hello': 'world'
                    })

                    result = fs.read(path)

                    assert result == '{"foo": "bar", "hello": "world"}'


def test_load_remote_env_vars(server):
    '''
    Test load_remote_env_vars() loads remote .env file
    and returns it as dict().
    '''
    for uid in server.users:
        path = os.path.join(server.ROOT_DIR, 'test.env')
        fs.write(path, REMOTE_ENV_FILE)

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_sftp_client') as rsc_m:
                rsc_m.return_value = client.open_sftp()
                result = buildman.load_remote_env_vars(path)

                assert result['FOO'] == 'bar'
                assert result['GREETING'] == 'Hello World'


def test_delete_old_builds(server):
    '''
    Test delete_old_builds() deletes old builds from the remote filesystem.
    '''
    history = {
        'builds': [
            {'id': '1'},
            {'id': '2'}
        ]
    }

    for uid in server.users:
        # Build directory setup
        base_path = os.path.join(server.ROOT_DIR, 'builds')
        build_path1 = os.path.join(server.ROOT_DIR, 'builds/build-1')
        build_path2 = os.path.join(server.ROOT_DIR, 'builds/build-2')
        build_path3 = os.path.join(server.ROOT_DIR, 'builds/build-3')
        build_path4 = os.path.join(server.ROOT_DIR, 'builds/build-4')

        os.mkdir(base_path)
        os.mkdir(build_path1)
        os.mkdir(build_path2)
        os.mkdir(build_path3)
        os.mkdir(build_path4)

        with server.client(uid) as client:
            with patch('boss.api.deployment.buildman.get_release_dir') as grd_m:
                grd_m.return_value = base_path

                with patch('boss.api.ssh.resolve_client') as rc_m:
                    rc_m.return_value = client
                    assert fs.exists(build_path1)
                    assert fs.exists(build_path2)
                    assert fs.exists(build_path3)
                    assert fs.exists(build_path4)

                    buildman.delete_old_builds(history)

                    assert fs.exists(build_path1)
                    assert fs.exists(build_path2)
                    assert not fs.exists(build_path3)
                    assert not fs.exists(build_path4)
