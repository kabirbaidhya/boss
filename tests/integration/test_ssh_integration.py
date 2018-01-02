''' Integration tests for ssh module. '''


import os
from mock import patch

from boss.core import fs
from boss.api import ssh


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


def test_run(server):
    ''' Test run() executes a command over ssh. '''
    for uid in server.users:
        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client
                result = ssh.run('echo "hello"')

                assert 'hello' in result


def test_run_list_of_commands(server):
    ''' Test run() executes a series of commands over ssh. '''
    for uid in server.users:
        with server.client(uid) as client:
            with patch('boss.api.ssh.resolve_client') as rc_m:
                rc_m.return_value = client
                result = ssh.run([
                    'echo "hello"',
                    'echo "world"',
                    'echo "foo"',
                    'echo "bar"'
                ])

                assert result == ['hello', 'world', 'foo', 'bar']
