'''
Vault client util functions.
'''

import os
from hvac import Client
from hvac.exceptions import Forbidden, VaultError
from requests.exceptions import ConnectionError

from boss.core.output import info, halt


def connect():
    '''
    Connect to the vault server and return the
    connected vault client instance.
    '''

    url = os.environ.get('VAULT_ADDR')
    token = os.environ.get('VAULT_TOKEN')

    if not url or not token:
        halt(
            'Failed connecting to vault. ' +
            '`VAULT_ADDR` and `VAULT_TOKEN` must be set in your environment.'
        )

    return Client(url=url, token=token)


def read_secrets(path):
    ''' Read secrets from the given path. '''
    try:
        client = connect()
        result = client.read(path)

        if not result or not result.get('data'):
            return {}

        return result['data']
    except ConnectionError:
        halt(
            'Failed connecting to vault server at {}.'.format(
                os.environ.get('VAULT_ADDR')
            )
        )

    except Forbidden:
        halt(
            'Permission denied. ' +
            'Make sure the token is authorized to access `{}` on vault.'.format(
                path
            )
        )

    except VaultError as e:
        halt('Vault Error: ' + e.message)


def env_inject_secrets(path, silent=False):
    '''
    Read secrets from the vault (from the given path),
    and inject them into the environment as env vars.
    '''
    secrets = read_secrets(path)

    if not silent:
        info('Using secrets from vault ({})'.format(path))

    for key, value in secrets.iteritems():
        os.environ[key] = value
