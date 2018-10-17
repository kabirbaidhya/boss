''' File System utilities API. '''

import os
import time
from StringIO import StringIO

from fabric.api import hide, put, get
from fabric.contrib import files, project

from . import runner
from boss.core.util.string import strip_ansi
from boss.core.util.types import is_iterable, is_string


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

    removal_path = path

    # If path is not a string but a list of multiple paths,
    # remove them all.
    if is_iterable(path) and not is_string(path):
        removal_path = ' '.join(path)

    runner.run('rm -rf {}'.format(removal_path), remote=remote)


def chown(path, user, group=None, remote=True):
    ''' Change ownership of a path recursively to the specified user and group. '''
    if group:
        cmd = 'chown -R {0}:{1} {2}'.format(user, group, path)
    else:
        cmd = 'chown -R {0} {1}'.format(user, path)

    runner.run(cmd, remote=remote)


def tar_archive(name, path, remote=True):
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
        result = runner.run('ls -1 {}'.format(path), remote=remote)
        return strip_ansi(result).split()


def exists(path, remote=True):
    '''
    Check if the path exists in the remote or locally,
    depending upon the `remote` parameter.
    '''

    if remote:
        return files.exists(path)

    return os.path.exists(path)


def upload(local_path, remote_path):
    ''' Upload one or more files to a remote host. '''
    return put(local_path, remote_path)


def upload_dir(local_dir, remote_dir):
    ''' Uploads a local directory to the remote path. '''
    project.upload_project(local_dir, remote_dir)


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
