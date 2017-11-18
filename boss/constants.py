''' Application wide common constants module. '''

# Predefined deployment presets
PRESET_WEB = 'web'
PRESET_NODE = 'node'
PRESET_REMOTE_SOURCE = 'remote-source'

# Default boss configuration
DEFAULT_CONFIG_FILE = 'boss.yml'
FABFILE_PATH = 'fabfile.py'
DEFAULT_CONFIG = {
    'user': 'boss',
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
    'stages': {},
    'scripts': {},
    'deployment': {
        'preset': PRESET_REMOTE_SOURCE,
        'build_dir': None,
        'base_dir': '~/boss',
        'cache_builds': True,
        'keep_builds': 5,
        'include_files': []
    },
    'notifications': {
        'slack': {
            'enabled': False,
            'endpoint': '',
            'deploying_color': 'good',
            'deployed_color': '#764FA5',
            'base_url': 'https://hooks.slack.com/services'
        },
        'hipchat': {
            'enabled': False,
            'notify': True,
            'company_name': '',
            'room_id': '',
            'auth_token': '',
            'deploying_color': 'yellow',
            'deployed_color': 'green',
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


# Preset specific default configurations.
# These will override the DEFAULT_CONFIG values for the configured preset.
PRESET_SPECIFIC_DEFAULTS = {
    PRESET_REMOTE_SOURCE: {},
    PRESET_WEB: {
        'deployment': {
            'cache_builds': False
        }
    },
    PRESET_NODE: {
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
