'''
Module for utility functions

TODO: Have a separate package `util` and have sub modules under it
to better categorize utilities.
'''

from fabric.api import run as _run, local as _local, hide
from fabric.colors import red, green, yellow


def halt(msg):
    ''' Terminate the script execution with a message '''
    raise SystemExit(red(msg))


def echo(msg):
    ''' Pring a plain message on the console. '''
    print(msg)


def info(msg):
    ''' Print a message (Information) '''
    echo('\n' + green(msg))


def host_print(msg, remote=True, leading_chars='\n'):
    ''' Print a raw message on the host. '''
    cmd = 'echo "{0}{1}"'.format(leading_chars, msg)

    with hide('running'):
        if remote:
            _run(cmd)
        else:
            _local(cmd)


def host_info(msg, remote=True):
    ''' Print a message (Information) on the host. '''
    host_print(green(msg), remote=remote)


def remote_print(msg):
    ''' Print a raw message on the remote logs. '''
    host_print(msg, remote=True)


def remote_info(msg):
    ''' Print a message (Information) on the remote logs. '''
    host_info(msg, remote=True)


def warn(msg):
    ''' Print a warning message. '''
    print('\n' + yellow(msg))


def warn_deprecated(msg):
    ''' Print a deprecated warning message. '''
    warn('Deprecated: {}'.format(msg))
