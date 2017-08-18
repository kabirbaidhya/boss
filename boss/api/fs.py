''' File System utilities API. '''

import time


def get_temp_filename(prefix=''):
    ''' Get a unique temporary filename. '''
    return '/tmp/' + (prefix + str(time.time()).replace('.', '-'))
