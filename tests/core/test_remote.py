'''
Tests for the boss.core.remote module.
'''

import pytest
from mock import Mock
from boss.core.remote import put


@pytest.fixture()
def callback():
    return lambda x, y: None


def test_put(callback):
    ''' Test put() works. '''
    sftp_client = Mock()
    local_path = 'test.yml'
    remote_path = '~/test.yml'

    put(
        sftp_client,
        local_path=local_path,
        remote_path=remote_path,
        callback=callback,
        confirm=False
    )
    sftp_client.put.assert_called_with(
        local_path,
        remote_path,
        callback,
        False
    )
