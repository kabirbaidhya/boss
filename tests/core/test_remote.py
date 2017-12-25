'''
Tests for the boss.core.remote module.
'''

import pytest
from mock import Mock
from boss.core import remote


@pytest.fixture()
def callback():
    ''' Callback to be used for sftp get() and put(). '''
    return lambda x, y: None


@pytest.fixture()
def sftp():
    ''' Get the mocked sftp client. '''
    return Mock()


@pytest.fixture()
def client():
    ''' Get the mocked ssh client. '''
    return Mock()


def test_put(sftp, callback):
    ''' Test put() works. '''
    local_path = 'test.yml'
    remote_path = '/path/to/test.yml'

    remote.put(
        sftp,
        local_path=local_path,
        remote_path=remote_path,
        callback=callback,
        confirm=False
    )
    sftp.put.assert_called_with(local_path, remote_path, callback, False)


def test_get(sftp, callback):
    ''' Test get() works. '''
    local_path = 'test.yml'
    remote_path = '/path/to/test.yml'

    remote.get(
        sftp,
        remote_path=remote_path,
        local_path=local_path,
        callback=callback
    )
    sftp.get.assert_called_with(remote_path, local_path, callback)


def test_run(client):
    ''' Test run() works. '''
    command = 'python --version'
    remote.run(client, command)
    client.exec_command.assert_called_with(
        command,
        bufsize=None,
        timeout=None,
        environment=None
    )


def test_run_with_environment(client):
    ''' Test run() works with env vars. '''
    command = 'npm start'
    remote.run(client, command, env={'NODE_ENV': 'production'})
    client.exec_command.assert_called_with(
        command,
        bufsize=None,
        timeout=None,
        environment={'NODE_ENV': 'production'}
    )
