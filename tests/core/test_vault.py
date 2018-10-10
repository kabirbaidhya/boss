''' Unit tests for boss.core.vault. '''

import os

from mock import Mock
from boss.core import vault
from boss.core.util.types import is_dict


def test_read_secrets():
    '''
    Test read_secrets() returns the secrets loaded from vault.
    '''
    path = 'test/vault/path'
    client = Mock()
    client.read.return_value = {
        'auth': None,
        'data': {
            'FOO': 'foo',
            'BAR': 'bar'
        }
    }
    result = vault.read_secrets(client, path)

    client.read.assert_called_with(path)
    assert result['FOO'] == 'foo'
    assert result['BAR'] == 'bar'


def test_read_secrets_with_no_response():
    '''
    Test read_secrets() still returns a dictionary (empty) for empty response.
    '''
    client = Mock()
    client.read.return_value = None

    result = vault.read_secrets(client, '')
    assert result is not None
    assert is_dict(result)


def test_read_secrets_with_no_data():
    '''
    Test read_secrets() still returns a dictionary (empty) for response with no data.
    '''
    client = Mock()
    client.read.return_value = {'data': None}

    result = vault.read_secrets(client, '')
    assert result is not None
    assert is_dict(result)


def test_env_inject_secrets():
    ''' Test env_inject_secrets() sets the env vars from vault. '''
    assert not os.environ.get('TEST_FOO')
    assert not os.environ.get('TEST_BAR')

    client = Mock()

    client.read.return_value = {
        'auth': None,
        'data': {
            'TEST_FOO': 'foo',
            'TEST_BAR': 'bar'
        }
    }

    vault.env_inject_secrets(client, 'path')
    client.read.assert_called_with('path')

    assert os.environ['TEST_FOO'] == 'foo'
    assert os.environ['TEST_BAR'] == 'bar'

    os.environ['TEST_FOO'] = ''
    os.environ['TEST_BAR'] = ''
