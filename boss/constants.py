''' Application wide common constants module. '''

DEFAULT_CONFIG_FILE = 'boss.yml'
DEFAULT_CONFIG = {
    'user': 'boss',
    'port': 22,
    'app_dir': '~/',
    'branch': 'dev',
    'repository_url': '',
    'project_name': 'untitled',
    'project_description': '',
    'branch_url': '{repository_url}/branch/{branch}',
    'service': None,
    'stages': {},
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
