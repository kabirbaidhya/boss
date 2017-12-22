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
