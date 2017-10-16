''' The configuration specific Module. '''

import os
from copy import deepcopy

import yaml
import dotenv
from .util import halt, merge
from .constants import DEFAULT_CONFIG, DEFAULT_CONFIG_FILE
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

    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)

    elif os.path.exists(fallback_path):
        dotenv.load_dotenv(fallback_path)


def load(filename=DEFAULT_CONFIG_FILE, stage=None):
    ''' Load the configuration and return it. '''
    try:
        with open(filename) as file_contents:
            resolve_dotenv_file(os.path.dirname(filename), stage)

            # Expand the environment variables used in the yaml config.
            loaded_config = os.path.expandvars(file_contents.read())

            # Parse the yaml configuration.
            loaded_config = yaml.load(loaded_config)
            merged_config = merge(DEFAULT_CONFIG, loaded_config)
            _config.update(merged_config)

            # Add base config to each of the stage config
            for (stage_name, _) in _config['stages'].items():
                _config['stages'][stage_name].update(
                    get_stage_config(stage_name))

            return get()

    except IOError:
        halt('Error loading config file "%s"' % filename)


def get_base_config():
    ''' Get the base configuration. '''
    return {
        'user': _config.get('user'),
        'port': _config.get('port'),
        'branch': _config.get('branch'),
        'app_dir': _config.get('app_dir'),
        'repository_url': _config.get('repository_url'),
        'deployment': _config.get('deployment')
    }


def get_stage_config(stage):
    ''' Retrieve the configuration for the given stage. '''
    try:
        stage_config = _config['stages'][stage]
        base_config = get_base_config()

        return merge(base_config, stage_config)
    except KeyError:
        halt('Unknown stage %s. Stage should be any one of %s' % (
            stage, _config['stages'].keys()
        ))


def fallback_branch(stage):
    ''' Get the fallback branch for the stage. '''
    return get_stage_config(stage).get('branch') or _config['branch']


def get_branch_url(branch):
    ''' Get the branch url to view it on the Web (eg: GitHub, GitLab etc.). '''
    return _config['branch_url'].format(
        repository_url=_config['repository_url'],
        branch=branch
    )
