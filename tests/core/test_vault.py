''' Unit tests for boss.core.vault. '''

import os

from mock import Mock, patch
from boss.core import vault
from boss.core.util.types import is_dict


@patch('boss.core.vault.connect')
def test_read_secrets(connect_m):
    '''
    Test read_secrets() returns the secrets loaded from vault.
    '''
    client = Mock()
    connect_m.return_value = client
    client.read.return_value = {
        'auth': None,
        'data': {
            'FOO': 'foo',
            'BAR': 'bar'
        }
    }
    result = vault.read_secrets('test/vault/path')

    client.read.assert_called_with('test/vault/path')
    assert result['FOO'] == 'foo'
    assert result['BAR'] == 'bar'


@patch('boss.core.vault.connect')
def test_read_secrets_with_no_response(connect_m):
    '''
    Test read_secrets() still returns a dictionary (empty) for empty response.
    '''
    client = Mock()
    connect_m.return_value = client
    client.read.return_value = None

    result = vault.read_secrets('')
    assert result is not None
    assert is_dict(result)


@patch('boss.core.vault.connect')
def test_read_secrets_with_no_data(connect_m):
    '''
    Test read_secrets() still returns a dictionary (empty) for response with no data.
    '''
    client = Mock()
    connect_m.return_value = client
    client.read.return_value = {'data': None}

    result = vault.read_secrets('')
    assert result is not None
    assert is_dict(result)


@patch('boss.core.vault.connect')
def test_env_inject_secrets(connect_m):
    ''' Test env_inject_secrets() sets the env vars from vault. '''
    assert not os.environ.get('TEST_FOO')
    assert not os.environ.get('TEST_BAR')

    client = Mock()
    connect_m.return_value = client
    client.read.return_value = {
        'auth': None,
        'data': {
            'TEST_FOO': 'foo',
            'TEST_BAR': 'bar'
        }
    }

    vault.env_inject_secrets('path')
    client.read.assert_called_with('path')

    assert os.environ['TEST_FOO'] == 'foo'
    assert os.environ['TEST_BAR'] == 'bar'

    os.environ['TEST_FOO'] = ''
    os.environ['TEST_BAR'] = ''
