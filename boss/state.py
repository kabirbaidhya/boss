''' Boss State. '''
from copy import deepcopy

_state = {}


def get():
    ''' Return the current boss state. '''
    return deepcopy(_state)
