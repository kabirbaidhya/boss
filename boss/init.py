''' Initialization module. '''

import sys
from fabric.api import env, task
from fabric.tasks import _is_task

from .util import warn_deprecated
from .config import load as load_config, get as get_config, get_stage_config
from .api.shell import get_stage
from .api.deployment import deployer


def init(module_name):
    ''' Initialize the boss configuration. '''
    config = load_config()

    # This service config option makes it too tightly coupled with
    # systemd services, so we'll need to make deployment process
    # independent of systemctl.
    if config['service'] is not None:
        warn_deprecated(
            'The `service` configuration option is deprecated' +
            ' and will be removed in the future releases.'
        )

    stage = get_stage()
    module = sys.modules[module_name]
    define_stage_tasks(module, config)
    define_preset_tasks(module, config)

    return (config, stage)


def define_preset_tasks(module, config):
    ''' Define tasks for the configured deployment preset. '''
    deployment = deployer.import_preset(config)
    # Now that we have deployment preset set, import all the tasks.
    for (task_name, func) in deployment.__dict__.iteritems():
        if not _is_task(func):
            continue

        # Set a new task named as the stage name in the main fabfile module.
        setattr(module, task_name, func)


def define_stage_tasks(module, config):
    ''' Define tasks for the stages dynamically. '''
    for (stage_name, _) in config['stages'].iteritems():
        task_func = task(name=stage_name)(configure_env)
        task_func.__doc__ = 'Configures the {} server environment.'.format(
            stage_name)

        # Set a new task named as the stage name in the main fabfile module.
        setattr(module, stage_name, task_func)


def configure_env():
    ''' Configures the fabric env. '''
    config = get_config()
    stage = get_stage()
    stage_config = get_stage_config(stage)
    env.user = stage_config.get('user') or config['user']
    env.port = stage_config.get('port') or config['port']
    env.cwd = stage_config.get('app_dir') or config['app_dir']
    env.key_filename = stage_config.get(
        'key_filename') or config['key_filename']
    env.hosts = [stage_config['host']]
