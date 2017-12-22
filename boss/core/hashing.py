''' Common Hashing Utilities. '''

import hashlib


def md5(string):
    ''' Generate md5 hex digest value. '''
    m = hashlib.md5()
    m.update(string)

    return m.hexdigest()
