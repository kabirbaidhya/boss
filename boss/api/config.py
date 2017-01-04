
import yaml
from boss.util import halt
from boss import config as boss_config

DEFAULT_CONFIG_FILE = 'boss.yml'


def get_default():
    return {
        'app_dir': '',
        'repository_url': '',
        'service': '',
        'stages': {},
        'services': {
            'slack': {
                'enabled': False,
                'endpoint': ''
            },
            'hipchat': {
                'enabled': False,
                'endpoint': ''
            }
        }
    }


def load(filename=DEFAULT_CONFIG_FILE):
    config = get_default()

    try:
        with open(filename) as file_contents:
            loaded_config = yaml.load(file_contents)
            config.update(loaded_config)
            boss_config.update(config)

        return config

    except IOError:
        halt('Error loading config file "%s"' % filename)
