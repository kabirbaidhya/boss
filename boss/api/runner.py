
from fabric.api import run as _run, local as _local
from ..config import get as _get_config


def run(command, remote=True):
    ''' Run a command using fabric. '''
    if remote:
        _run(command)
    else:
        _local(command)


def is_script_defined(script):
    ''' Check if the script is defined in the config. '''
    custom_scripts = _get_config()['scripts']

    return custom_scripts.has_key(script)


def run_script_safely(script, remote=True):
    '''
    Run a script only if it is defined in the config.
    Otherwise, it's skipped without throwing an error.
    '''
    if is_script_defined(script):
        run_script(script, remote)


def run_script(script, remote=True):
    ''' Run a script. '''
    custom_scripts = _get_config()['scripts']

    # If the script is not defined raise error.
    if not is_script_defined(script):
        raise RuntimeError('Missing script "{}"'.format(script))

    # Get the command defined in the script.
    script_cmd = custom_scripts[script]

    # Run a custom script defined in the config.
    run(script_cmd, remote)
