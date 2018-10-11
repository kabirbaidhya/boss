'''
Vault client util functions.
'''
import os
from boss.core.output import info, halt
from hvac import Client


def connect(silent=False):
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

    if not silent:
        info('Connecting to vault')

    return Client(url=url, token=token)


def read_secrets(path, silent=False):
    ''' Read secrets from the given path. '''
    client = connect(silent)

    if not silent:
        info('Reading vault secrets from: {}'.format(path))

    result = client.read(path)

    if not result or not result.get('data'):
        return {}

    return result['data']


def env_inject_secrets(path, silent=False):
    '''
    Read secrets from the vault (from the given path),
    and inject them into the environment as env vars.
    '''
    secrets = read_secrets(path, silent)

    if not silent:
        info('Using env vars from vault')

    for key, value in secrets.iteritems():
        os.environ[key] = value
