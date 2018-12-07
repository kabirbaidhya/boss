''' Unit tests for boss.core.vault. '''

import os
import pytest
from mock import Mock, patch
from requests.exceptions import ConnectionError
from hvac.exceptions import Forbidden, VaultError

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

    vault.env_inject_secrets('path', True)
    client.read.assert_called_with('path')

    assert os.environ['TEST_FOO'] == 'foo'
    assert os.environ['TEST_BAR'] == 'bar'

    os.environ['TEST_FOO'] = ''
    os.environ['TEST_BAR'] = ''


@patch('boss.core.vault.Client')
def test_env_inject_secrets_with_output(client_m, capsys):
    '''
    Test env_inject_secrets() with silent=False prints output.
    '''

    os.environ['VAULT_ADDR'] = 'vault_addr'
    os.environ['VAULT_TOKEN'] = 'vault_token'

    client = Mock()
    client_m.return_value = client
    client.read.return_value = {}

    vault.env_inject_secrets('vault/path', silent=False)
    client.read.assert_called_with('vault/path')

    out, _ = capsys.readouterr()

    assert 'Using secrets from vault (vault/path)' in out


@patch('boss.core.vault.Client')
def test_env_inject_secrets_in_silent_mode(client_m, capsys):
    '''
    Test env_inject_secrets() with silent=True prints no output.
    '''

    os.environ['VAULT_ADDR'] = 'vault_addr'
    os.environ['VAULT_TOKEN'] = 'vault_token'

    client = Mock()
    client_m.return_value = client
    client.read.return_value = {}

    vault.env_inject_secrets('vault/path', silent=True)
    client.read.assert_called_with('vault/path')

    out, _ = capsys.readouterr()

    assert out.strip() == ''


@patch('boss.core.vault.Client')
def test_connect_throws_error(client_m):
    '''
    Test connect() throws error if
    VAULT_ADDR and VAULT_TOKEN not found in the environment.
    '''

    os.environ['VAULT_ADDR'] = ''
    os.environ['VAULT_TOKEN'] = ''

    error_message = (
        'Failed connecting to vault. ' +
        '`VAULT_ADDR` and `VAULT_TOKEN` must be set in your environment.'
    )
    with pytest.raises(SystemExit, match=error_message):
        vault.connect()

    client_m.assert_not_called()


@patch('boss.core.vault.connect')
def test_read_secrets_shows_vault_connection_error(connect_m):
    '''
    Test read_secrets() gracefully displays vault errors.
    '''
    os.environ['VAULT_ADDR'] = 'https://test.vaultserver'
    connect_m.side_effect = ConnectionError('Boom!')

    error_message = 'Failed connecting to vault server at .*'
    with pytest.raises(SystemExit, match=error_message):
        vault.read_secrets('test/vault/path')


@patch('boss.core.vault.connect')
def test_read_secrets_shows_vault_forbidden_error(connect_m):
    '''
    Test read_secrets() gracefully displays vault errors.
    '''
    os.environ['VAULT_ADDR'] = 'https://test.vaultserver'
    connect_m.side_effect = Forbidden('Boom!')

    error_message = (
        'Permission denied. ' +
        'Make sure the token is authorized to access `test/vault/path`.*'
    )
    with pytest.raises(SystemExit, match=error_message):
        vault.read_secrets('test/vault/path')


@patch('boss.core.vault.connect')
def test_read_secrets_shows_vault_vault_error(connect_m):
    '''
    Test read_secrets() gracefully displays vault errors.
    '''
    os.environ['VAULT_ADDR'] = 'https://test.vaultserver'
    connect_m.side_effect = VaultError('Boom!')

    error_message = 'Vault Error: Boom!'
    with pytest.raises(SystemExit, match=error_message):
        vault.read_secrets('test/vault/path')
