''' Object utility functions. '''

import collections
from copy import deepcopy


def merge(dict1, dict2):
    '''
    Merge two dictionaries recursively and
    return the merged dict. (Immutable)
    '''
    result = deepcopy(dict1)

    for key, value in dict2.iteritems():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result
