''' Integration tests for boss.api.fs module. '''


import os
from mock import patch

from boss.core import fs
from boss.api.fs import rm_rf, glob


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

                rm_rf([path1, path2])

                assert not fs.exists(path1)
                assert not fs.exists(path2)


def test_glob(server):
    ''' Test glob() gets a list of files and directories from the remote. '''
    for uid in server.users:
        base_path = os.path.join(server.ROOT_DIR, 'base')
        path1 = os.path.join(server.ROOT_DIR, 'base/test1')
        path2 = os.path.join(server.ROOT_DIR, 'base/test2')
        path3 = os.path.join(server.ROOT_DIR, 'base/abc.txt')
        path4 = os.path.join(server.ROOT_DIR, 'base/xyz.txt')

        os.mkdir(base_path)
        os.mkdir(path1)
        os.mkdir(path2)
        fs.write(path3, 'Foo')
        fs.write(path4, 'Bar')

        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client
                assert fs.exists(path1)
                assert fs.exists(path2)
                assert fs.exists(path3)
                assert fs.exists(path4)

                result = glob(base_path)
                expected = ['test1', 'test2', 'abc.txt', 'xyz.txt']

                assert sorted(result) == sorted(expected)
