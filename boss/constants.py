''' Application wide common constants module. '''

from os.path import expanduser
from boss.core.constants import ci
from boss.core.constants.presets import (
    WEB,
    NODE,
    REMOTE_SOURCE
)

# Predefined deployment presets

# Default boss configuration
DEFAULT_CONFIG_FILE = 'boss.yml'
FABFILE_PATH = 'fabfile.py'

# Boss paths
BOSS_HOME_PATH = expanduser('~/.boss')
BOSS_CACHE_PATH = BOSS_HOME_PATH + '/cache'

DEFAULT_CONFIG = {
    'user': 'app',
    'port': 22,
    'key_filename': '~/.ssh/id_rsa',
    'ssh_forward_agent': False,
    'verbose_logging': False,
    'app_dir': '~/',
    'branch': 'master',
    'repository_url': '',
    'project_name': 'untitled',
    'project_description': '',
    'branch_url': '{repository_url}/branch/{branch}',
    'remote_env_injection': False,
    'remote_env_path': None,
    'stages': {},
    'scripts': {},
    'ci': {
        'base_url': ci.TRAVIS_PAID_BASE_URL
    },
    'deployment': {
        'preset': REMOTE_SOURCE,
        'build_dir': None,
        'base_dir': '~/deployment',
        'keep_builds': 5,
        'include_files': []
    },
    'notifications': {
        'slack': {
            'enabled': False,
            'endpoint': '',
            'deploying_color': 'good',
            'deployed_color': '#764FA5',
            'ci_deploying_color': '#cccccc',
            'ci_deployed_color': '#7CD197',
            'base_url': 'https://hooks.slack.com/services'
        },
        'hipchat': {
            'enabled': False,
            'notify': True,
            'company_name': '',
            'room_id': '',
            'auth_token': '',
            'deploying_color': 'green',
            'deployed_color': 'purple',
            'ci_deploying_color': 'gray',
            'ci_deployed_color': 'yellow',
        }
    }
}

# Predefined custom scripts/hooks
SCRIPT_STOP = 'stop'
SCRIPT_LOGS = 'logs'
SCRIPT_START = 'start'
SCRIPT_BUILD = 'build'
SCRIPT_RELOAD = 'reload'
SCRIPT_INSTALL = 'install'
SCRIPT_STATUS_CHECK = 'status_check'
SCRIPT_LIST_SERVICES = 'list_services'
SCRIPT_INSTALL_REMOTE = 'install_remote'
SCRIPT_START_OR_RELOAD = 'start_or_reload'


# Preset specific defaults
PRESET_SPECIFIC_DEFAULTS = {
    REMOTE_SOURCE: {},
    WEB: {},
    NODE: {
        'deployment': {
            'include_files': [
                'package.json', 'package-lock.json', 'yarn.lock', 'pm2.config.js'
            ]
        },
        'scripts': {
            SCRIPT_INSTALL: 'npm install',
            SCRIPT_INSTALL_REMOTE: 'npm install',
            SCRIPT_BUILD: 'npm run build'
            # TODO: Add pm2 based scripts too as a default.
        }
    }
}
