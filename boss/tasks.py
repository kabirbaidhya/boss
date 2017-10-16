'''
Boss default tasks module.
'''

from fabric.api import run as _run, task
import boss.constants as constants
from .util import halt
from .api import shell, runner
from .config import get_stage_config, get as get_config


@task
def logs():
    ''' Tail the logs. '''
    stage = shell.get_stage()
    stage_specific_logging = get_stage_config(stage).get('logging')
    logging_config = stage_specific_logging or get_config().get('logging')

    # If log files are configured tail them.
    if logging_config and logging_config.get('files'):
        # Tail the logs from log files
        log_paths = ' '.join(logging_config.get('files'))
        _run('tail -f ' + log_paths)
        return

    # If logs script is defined, run it
    runner.run_script_safely(constants.SCRIPT_LOGS)


@task
def run(script):
    ''' Run a custom script. '''
    # Run a custom script defined in the config.
    try:
        runner.run_script(script)
    except RuntimeError as e:
        halt(str(e))

__all__ = ['run', 'logs']
