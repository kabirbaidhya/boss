''' The configuration specific Module. '''

from copy import deepcopy
import yaml
from .util import halt, merge
from .constants import DEFAULT_CONFIG, DEFAULT_CONFIG_FILE

_config = deepcopy(DEFAULT_CONFIG)


def get():
    '''
    Return the loaded configuration.
    Note: The returned config is a deep clone of the original config.
    '''
    return deepcopy(_config)


def load(filename=DEFAULT_CONFIG_FILE):
    ''' Load the configuration and return it. '''
    try:
        with open(filename) as file_contents:
            loaded_config = yaml.load(file_contents)
            merged_config = merge(DEFAULT_CONFIG, loaded_config)
            _config.update(merged_config)

            # Add base config to each of the stage config
            for (stage, stage_config) in _config['stages'].items():
                _config['stages'][stage].update(get_stage_config(stage))

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
        'repository_url': _config.get('app_dir')
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


def get_service():
    ''' Return the configured service name.'''
    return _config['service']


def fallback_branch(stage):
    ''' Get the fallback branch for the stage. '''
    return get_stage_config(stage).get('branch') or _config['branch']


def get_branch_url(branch):
    ''' Get the branch url to view it on the Web (eg: GitHub, GitLab etc.). '''
    return _config['branch_url'].format(
        repository_url=_config['repository_url'],
        branch=branch
    )
