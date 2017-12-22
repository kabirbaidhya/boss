'''
Boss core file system utilities.
'''
import os
import tarfile


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
