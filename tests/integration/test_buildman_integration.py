'''
Integration tests for buildman.
TODO: Replace mock-ssh-server with some other alternatives.
'''

import os
from mock import patch
from boss.core import fs
from boss.api.deployment import buildman


def test_load_history(server):
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
