''' File System utilities over SSH for the Remote end. '''

import time

from boss.api import ssh
from boss.core.util.string import strip_ansi
from boss.core.util.types import is_iterable, is_string


def get_temp_filename(prefix=''):
    ''' Get a unique temporary filename. '''
    return '/tmp/' + (prefix + str(time.time()).replace('.', '-'))


def mkdir(path, nested=False):
    ''' Create a new directory. '''
    options = '-p ' if nested else ''
    cmd = 'mkdir {0}{1}'.format(options, path)

    # Run the command.
    ssh.run(cmd)


def rm(path):
    ''' Remove a file given by the path. '''
    ssh.run('rm ' + path)


def rm_rf(path):
    ''' Remote the specified path recursively (both files and directories). '''
    removal_path = path

    # If path is not a string but a list of multiple paths,
    # remove them all.
    if is_iterable(path) and not is_string(path):
        removal_path = ' '.join(path)

    return ssh.run('rm -rf {}'.format(removal_path))


def chown(path, user, group=None):
    ''' Change ownership of a path recursively to the specified user and group. '''
    if group:
        cmd = 'chown -R {0}:{1} {2}'.format(user, group, path)
    else:
        cmd = 'chown -R {0} {1}'.format(user, path)

    ssh.run(cmd)


def tar_archive(name, path):
    ''' Compress the source path into a tar archive. '''
    cmd = 'tar -czvf {} {}'.format(name, path)

    ssh.run(cmd)


def tar_extract(src, dest):
    ''' Extract a source tar archive to the specified destination path. '''
    cmd = 'tar zxvf {} --strip-components=1 -C {}'.format(src, dest)
    ssh.run(cmd)


def glob(path):
    ''' Glob a directory path to get the list of files. '''
    result = ssh.run('ls -1 {}'.format(path))

    return map(strip_ansi, result)


def exists(path):
    '''
    Check if the path exists in the remote.
    '''
    return ssh.exists(path)


def upload(local_path, remote_path):
    ''' Upload one or more files to a remote host. '''
    return ssh.put(local_path, remote_path)


def upload_dir(local_dir, remote_dir):
    ''' Uploads a local directory to the remote path. '''
    return ssh.upload_dir(local_dir, remote_dir)


def update_symlink(src, link_path):
    ''' Update the current build symlink. '''
    cmd = 'ln -sfn {} {}'.format(src, link_path)
    ssh.run(cmd)
