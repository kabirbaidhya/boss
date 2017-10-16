''' Application wide common constants module. '''

# Predefined deployment presets
PRESET_WEB = 'web'
PRESET_NODE = 'node'
PRESET_REMOTE_SOURCE = 'remote-source'

# Default boss configuration
DEFAULT_CONFIG_FILE = 'boss.yml'
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
        'build_dir': 'build/',
        'base_dir': '~/boss',
        'keep_builds': 3,
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
