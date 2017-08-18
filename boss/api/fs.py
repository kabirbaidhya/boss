''' File System utilities API. '''

import time
from . import runner


def get_temp_filename(prefix=''):
    ''' Get a unique temporary filename. '''
    return '/tmp/' + (prefix + str(time.time()).replace('.', '-'))


def mkdir(path, remote=True, nested=True):
    ''' Create a new directory. '''
    options = '-p ' if nested else ''
    cmd = 'mkdir {0}{1}'.format(options, path)

    # Run the command.
    runner.run(cmd, remote=remote)
