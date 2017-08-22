'''
Module for utility functions

TODO: Have a separate package `util` and have sub modules under it
to better categorize utilities.
'''

import time
import collections
from datetime import datetime
from copy import deepcopy
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


def is_string(obj):
    ''' Check if the object is a string. '''
    return isinstance(obj, basestring)


def is_iterable(obj):
    ''' Check if the object is iterable. '''
    return hasattr(obj, '__iter__')


def merge(dict1, dict2):
    ''' Merge Two dictionaries recursively. '''
    result = deepcopy(dict1)

    for key, value in dict2.iteritems():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result


def localize_utc_timestamp(utc_datetime):
    ''' Convert timestamp in UTC to local timezone. '''
    now = time.time()
    offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
    return utc_datetime + offset
