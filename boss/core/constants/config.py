''' Configuration Constants. '''

from . import ci, presets
from .known_scripts import (INSTALL, INSTALL_REMOTE)


DEFAULT_CONFIG = {
    'user': 'app',
    'port': 22,
    'cwd': None,
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
    'vault': {
        'enabled': False,
        'path': 'secret',
        'silent': False
    },
    'ci': {
        'base_url': ci.TRAVIS_PAID_BASE_URL
    },
    'deployment': {
        'preset': presets.REMOTE_SOURCE,
        'build_dir': None,
        'base_dir': '~/deployment',
        'keep_builds': 5,
        'include_files': [],
        'smart_install': False,
        'use_local_ref': True
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
        'smart_install': True,
        'include_files': [
            'package.json', 'package-lock.json', 'yarn.lock', 'pm2.config.js'
        ]
    },
    'scripts': {
        INSTALL: 'npm install',
        INSTALL_REMOTE: 'npm install'
    }
}
