''' The configuration specific Module. '''

import os
import yaml
import dotenv
from copy import deepcopy


from .constants import DEFAULT_CONFIG_FILE
from .core import fs
from .core.output import halt, info
from .core.util.object import merge
from .core.util.colors import cyan
from .core.constants.config import DEFAULT_CONFIG, PSD


_config = deepcopy(DEFAULT_CONFIG)


def get():
    '''
    Return the loaded configuration.
    Note: The returned config is a deep clone of the original config.
    '''
    return deepcopy(_config)


def resolve_dotenv_file(path, stage=None):
    '''
    Resolve dotenv file and load environment vars if it exists.
    If stage parameter is provided, then stage specific .env file is resolved,
    for instance .env.production if stage=production etc.
    If stage is None, just .env file is resolved.
    '''
    filename = '.env' + ('' if not stage else '.{}'.format(stage))
    dotenv_path = os.path.join(path, filename)
    fallback_path = os.path.join(path, '.env')

    if fs.exists(dotenv_path):
        info('Resolving env file: {}'.format(cyan(dotenv_path)))
        dotenv.load_dotenv(dotenv_path)

    elif fs.exists(fallback_path):
        info('Resolving env file: {}'.format(cyan(fallback_path)))
        dotenv.load_dotenv(fallback_path)


def get_deployment_preset(raw_config):
    ''' Get the deployment preset for a raw config. '''
    has_preset = (
        isinstance(raw_config.get('deployment'), dict) and
        'preset' in raw_config.get('deployment')
    )

    # If preset is configured return it.
    if has_preset:
        return raw_config['deployment']['preset']

    # Else return the default deployment config preset.
    return DEFAULT_CONFIG['deployment']['preset']


def merge_config(raw_config):
    '''
    Merge the default and preset specific default configs,
    to the raw configuration, add stage default configuration
    to each stage too and return the merged result.
    '''
    preset = get_deployment_preset(raw_config)
    preset_defaults = PSD[preset]
    all_defaults = merge(DEFAULT_CONFIG, preset_defaults)
    result = merge(all_defaults, raw_config)
    base_config = get_base_config(result)

    # Add base config to each of the stage config
    for (stage_name, _) in result['stages'].items():
        stage_config = result['stages'][stage_name]
        merged_stage_config = merge(base_config, stage_config)
        result['stages'][stage_name].update(merged_stage_config)

    return result


def load(filename=DEFAULT_CONFIG_FILE, stage=None):
    ''' Load the configuration and return it. '''
    try:
        # pass
        file_contents = fs.read(filename)
        resolve_dotenv_file(os.path.dirname(filename), stage)

        # Expand the environment variables used in the yaml config.
        loaded_config = os.path.expandvars(file_contents)

        # Parse the yaml configuration.
        # And merge it with the defaults before it's used everywhere.
        loaded_config = yaml.load(loaded_config)
        merged_config = merge_config(loaded_config)

        _config.update(merged_config)

        return get()

    except KeyError:
        halt('Invalid configuration file "{}"'.format(filename))

    except IOError:
        halt('Error loading config file "%s"' % filename)


def get_base_config(resolved_config=None):
    ''' Get the base configuration. '''
    config = resolved_config or _config

    return {
        'user': config.get('user'),
        'port': config.get('port'),
        'branch': config.get('branch'),
        'app_dir': config.get('app_dir'),
        'deployment': config.get('deployment'),
        'repository_url': config.get('repository_url'),
        'remote_env_path': config.get('remote_env_path')
    }


def get_stage_config(stage):
    ''' Retrieve the configuration for the given stage. '''
    try:
        return _config['stages'][stage]
    except KeyError:
        halt('Unknown stage %s. Stage should be any one of %s' % (
            stage, _config['stages'].keys()
        ))
