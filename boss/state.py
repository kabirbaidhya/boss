''' Boss State. '''
from copy import deepcopy


_state = {}


def get(key=None):
    '''
    Return the current boss state.

    If `key` is provided, returns a value in the state
    identified by `key`.'''

    from fabric import state as fabric_state

    merged_state = deepcopy(_state)
    merged_state['env'] = fabric_state.env
    merged_state['connections'] = fabric_state.connections

    if not key:
        return merged_state

    return merged_state[key]


# def get_fabric_state():
#     '''
#     Returns fabric state variables.

#     Note: Don't rely on this function, this will be removed in the future.
#     The purpose of this function is just to abstract over fabric's state,
#     instead of using fabric.state.* directly, so that it would be easier
#     to get rid of fabric in the future major releases.
#     '''
