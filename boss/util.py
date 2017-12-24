'''
Module for utility functions.

TODO: Remove all fabric dependant util functions.
'''

from fabric.api import run as _run, local as _local, hide

from boss.core.util.colors import green


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
