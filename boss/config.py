'''
The configuration specific Module.
'''

from copy import deepcopy
import yaml
from .util import halt, merge

DEFAULT_CONFIG = {
    'user': 'boss',
    'app_dir': '~/',
    'branch': 'dev',
    'repository_url': '',
    'service': '',
    'stages': {},
    'services': {
        'slack': {
            'enabled': False,
            'endpoint': '',
            'deploying_color': 'good',
            'deployed_color': '#764FA5',
            'base_uri': 'https://hooks.slack.com/services'
        },
        'hipchat': {
            'enabled': False,
            'endpoint': ''
        }
    }
}
DEFAULT_FILENAME = 'boss.yml'

_config = deepcopy(DEFAULT_CONFIG)


def get():
    '''
    Return the loaded configuration.
    Note: The returned config is a deep clone of the original config.
    '''
    return deepcopy(_config)


def load(filename=DEFAULT_FILENAME):
    ''' Load the configuration and return it. '''
    try:
        with open(filename) as file_contents:
            loaded_config = yaml.load(file_contents)
            merged_config = merge(DEFAULT_CONFIG, loaded_config)
            _config.update(merged_config)

            return get()

    except IOError:
        halt('Error loading config file "%s"' % filename)


def get_stage_config(stage):
    ''' Retrieve the configuration for the given stage. '''
    try:
        return _config['stages'][stage]
    except KeyError:
        halt('Unknown stage %s. Stage should be any one of %s' % (
            stage, _config['stages'].keys()
        ))
