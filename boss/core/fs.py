'''
Boss core file system utilities.
'''
import os
import tarfile
from time import time
from random import random


def read(filename):
    ''' Read contents of file and return it. '''
    with open(filename, 'r') as f:
        return f.read()


def write(filename, data):
    ''' Write data to the file. '''
    with open(filename, 'w') as f:
        f.write(data)


def exists(path):
    ''' Check if file path exists. '''
    return os.path.exists(path)


def compress(source_dir, filename):
    ''' Compress a directory and build an archive (Tar zipped). '''
    with tarfile.open(filename, 'w:gz') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def rm(path):
    ''' Remove a file given by the path. '''
    return os.remove(path)


def size_unit(size):
    '''
    Get a human readable size unit (eg: KB, MB, GB etc) for the
    given file size in bytes.
    '''
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(size) < 1024.0:
            return '%3.1f %s' % (size, unit)

        size /= 1024.0

    return '%.1f %s' % (size, 'YB')


def tmp_path():
    ''' Get a temp path. '''
    return '/tmp/' + str(time() * (1 + random())).replace('.', '')
