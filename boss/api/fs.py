''' File System utilities API. '''

import time
from StringIO import StringIO
from fabric.api import hide, put, get

from . import runner
from .. import util


def get_temp_filename(prefix=''):
    ''' Get a unique temporary filename. '''
    return '/tmp/' + (prefix + str(time.time()).replace('.', '-'))


def mkdir(path, remote=True, nested=False):
    ''' Create a new directory. '''
    options = '-p ' if nested else ''
    cmd = 'mkdir {0}{1}'.format(options, path)

    # Run the command.
    runner.run(cmd, remote=remote)


def rm(path, remote=True):
    ''' Remove a file given by the path. '''
    runner.run('rm ' + path, remote=remote)


def rm_rf(path, remote=True):
    ''' Remote the specified path recursively (both files and directories). '''

    files = path

    # If path is not a string but a list of multiple paths,
    # remove them all.
    if util.is_iterable(path) and not util.is_string(path):
        files = ' '.join(path)

    runner.run('rm -rf {}'.format(files), remote=remote)


def chown(path, user, group=None, remote=True):
    ''' Change ownership of a path recursively to the specified user and group. '''
    if group:
        cmd = 'chown -R {0}:{1} {2}'.format(user, group, path)
    else:
        cmd = 'chown -R {0} {1}'.format(user, path)

    runner.run(cmd, remote=remote)


def tar_archive(path, name, remote=True):
    ''' Compress the source path into a tar archive. '''
    cmd = 'tar -czvf {} {}'.format(name, path)

    with hide('stdout'):
        runner.run(cmd, remote=remote)


def tar_extract(src, dest, remote=True):
    ''' Extract a source tar archive to the specified destination path. '''
    cmd = 'tar zxvf {} --strip-components=1 -C {}'.format(src, dest)
    runner.run(cmd, remote=remote)


def glob(path, remote=True):
    ''' Glob a directory path to get the list of files. '''
    with hide('everything'):
        return runner.run('ls -1 {}'.format(path), remote=remote).split()


def save_remote_file(path, data):
    ''' Save data to the remote file. '''
    fd = StringIO(data)
    put(fd, path)

    return fd.getvalue()


def read_remote_file(path):
    ''' Read remote file contents. '''
    fd = StringIO()
    get(path, fd)

    return fd.getvalue()


def update_symlink(src, link_path, remote=True):
    ''' Update the current build symlink. '''
    cmd = 'ln -sfn {} {}'.format(src, link_path)
    runner.run(cmd, remote=remote)
