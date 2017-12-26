'''
Integration tests for buildman.
TODO: Replace mock-ssh-server with some other alternatives.
'''

import os
from mock import patch
from boss.core import fs
from boss.api.deployment import buildman


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
