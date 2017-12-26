''' Integration tests for boss.api.fs module. '''


import os
from mock import patch

from boss.core import fs
from boss.api.fs import rm_rf


def test_rm_rf(server):
    ''' Test rm_rf() removes multiple directories on the remote host. '''
    for uid in server.users:
        os.mkdir(os.path.join(server.ROOT_DIR, 'test1'))
        os.mkdir(os.path.join(server.ROOT_DIR, 'test2'))

        path1 = os.path.join(server.ROOT_DIR, 'test1/abc.txt')
        path2 = os.path.join(server.ROOT_DIR, 'test2/xyz.txt')

        fs.write(path1, 'Foo')
        fs.write(path2, 'Bar')

        with server.client(uid) as client:

            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client
                assert fs.exists(path1)
                assert fs.exists(path2)
                (_, stdout, _) = rm_rf([path1, path2])

                assert stdout.read() is not None
                assert not fs.exists(path1)
                assert not fs.exists(path2)
