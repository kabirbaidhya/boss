
from fabric.api import run as _run, local as _local, hide

from boss.api import notif, shell
from boss.util import host_info
from boss.config import get as _get_config
from boss.core.util.colors import cyan
from boss.core.constants.notification_types import (
    RUNNING_SCRIPT_STARTED,
    RUNNING_SCRIPT_FINISHED
)


def run(command, remote=True):
    ''' Run a command using fabric. '''
    if remote:
        return _run(command)
    else:
        return _local(command)


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


def should_notify(script):
    ''' Check if the script being run should be notified. '''
    notified_scripts = _get_config()['notified_hooks']['scripts']

    if notified_scripts == 'all':
        return True

    if script in notified_scripts:
        return True

    return False


def run_script(script, remote=True):
    ''' Run a script. '''
    custom_scripts = _get_config()['scripts']

    # If the script is not defined raise error.
    if not is_script_defined(script):
        raise RuntimeError('Missing script "{}"'.format(script))

    needs_notification = should_notify(script)

    if needs_notification:
        notif.send(RUNNING_SCRIPT_STARTED, {
            'script': script,
            'user': shell.get_user(),
            'stage': shell.get_stage()
        })

        # Get the command defined in the script.
    script_cmd = custom_scripts[script]

    info_text = 'Running {}\n{}'.format(
        cyan(script), cyan('> ' + script_cmd)
    )
    host_info(info_text, remote=remote)

    # Run a custom script defined in the config.
    with hide('running'):
        run(script_cmd, remote)

    if needs_notification:
        notif.send(RUNNING_SCRIPT_FINISHED, {
            'script': script,
            'user': shell.get_user(),
            'stage': shell.get_stage()
        })
