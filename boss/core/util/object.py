''' Object utility functions. '''

import collections
from copy import deepcopy


def merge(dict1, dict2):
    '''
    Merge two dictionaries recursively and
    return the merged dict. (Immutable)

    Note: dict2 overrides the keys of dict1 if they have same keys.
    '''
    result = deepcopy(dict1)

    for key, value in dict2.iteritems():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result


def with_only(src, attrs):
    '''
    Return a new copy of source dictionary
    containing only the attributes provided.
    '''
    result = {}

    for key, value in src.iteritems():
        if key in attrs:
            result[key] = value

    return result
