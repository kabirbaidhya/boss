''' Boss State. '''
from boss.util import merge

_state = {}


def get(key=None):
    '''
    Return the current boss state.

    If `key` is provided, returns a value in the state
    identified by `key`.'''

    fabric_state = get_fabric_state()
    merged_state = merge(fabric_state, _state)

    if not key:
        return merged_state

    return merged_state[key]


def get_fabric_state():
    '''
    Returns fabric state variables.

    Note: Don't rely on this function, this will be removed in the future.
    The purpose of this function is just to abstract over fabric's state,
    instead of using fabric.state.* directly, so that it would be easier
    to get rid of fabric in the future major releases.
    '''
    from fabric.state import env, connections

    return dict(
        env=env,
        connections=connections
    )
