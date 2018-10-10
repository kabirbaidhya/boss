'''
Vault client util functions.
'''
import os

from hvac import Client


def connect():
    '''
    Connect to the vault server and return the
    connected vault client instance.
    '''
    client = Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )

    return client


def read_secrets(client, path):
    ''' Read secrets from the given path. '''
    result = client.read(path)

    if not result or not result.get('data'):
        return {}

    return result['data']


def env_inject_secrets(client, path):
    '''
    Read secrets from the vault (from the given path),
    and inject them into the environment as env vars.
    '''
    secrets = read_secrets(client, path)

    for key, value in secrets.iteritems():
        os.environ[key] = value
