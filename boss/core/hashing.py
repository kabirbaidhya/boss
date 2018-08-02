''' Common Hashing Utilities. '''

import hashlib


def md5(string):
    ''' Generate md5 hex digest value from a string input. '''
    m = hashlib.md5()
    m.update(string)

    return m.hexdigest()
