''' Configuration Constants. '''

from . import ci, presets
from .known_scripts import (
    INSTALL,
    INSTALL_REMOTE,
    BUILD
)


DEFAULT_CONFIG = {
    'user': 'app',
    'port': 22,
    'cwd': '/home/app',
    'key_filename': '~/.ssh/id_rsa',
    'ssh_forward_agent': False,
    'verbose_logging': False,
    'branch': 'master',
    'repository_url': '',
    'project_name': None,
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
        'preset': presets.REMOTE_SOURCE,
        'build_dir': None,
        'base_dir': '~/deployment',
        'cache_builds': True,
        'keep_builds': 5,
        'include_files': [],
        'stage_independent_builds': True
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
    },
    'notified_hooks': {
        'scripts': []
    }
}


# Preset specific defaults
PSD = {}
PSD[presets.REMOTE_SOURCE] = {}
PSD[presets.WEB] = {}
PSD[presets.NODE] = {
    'deployment': {
        'include_files': [
            'package.json', 'package-lock.json', 'yarn.lock', 'pm2.config.js'
        ]
    },
    'scripts': {
        INSTALL: 'npm install',
        INSTALL_REMOTE: 'npm install',
        BUILD: 'npm run build'
    }
}
