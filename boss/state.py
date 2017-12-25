''' Boss State. '''

from copy import deepcopy


_state = {
    'sftp_connections': {}
}


def get(key=None):
    '''
    Return the current boss state.

    If `key` is provided, returns a value in the state
    identified by `key`.
    '''

    from fabric import state as fabric_state

    merged_state = deepcopy(_state)
    merged_state['env'] = fabric_state.env
    merged_state['connections'] = fabric_state.connections

    if not key:
        return merged_state

    return merged_state[key]


def replace(key, value):
    ''' Set or replace a key with the provided value in the state. '''
    _state[key] = value
