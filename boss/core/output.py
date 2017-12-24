''' Console output utilities. '''

from .util.colors import red, green, yellow


def halt(msg):
    ''' Terminate the script execution with a message '''
    raise SystemExit(red(msg))


def echo(msg):
    ''' Pring a plain message on the console. '''
    print(msg)


def info(msg):
    ''' Print a message (Information). '''
    echo('\n' + green(msg))


def warn(msg):
    ''' Print a warning message. '''
    echo('\n' + yellow(msg))


def warn_deprecated(msg):
    ''' Print a deprecated warning message. '''
    warn('Deprecated: {}'.format(msg))
