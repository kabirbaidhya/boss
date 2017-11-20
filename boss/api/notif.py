'''
Notification API module.
'''

from . import slack
from . import hipchat
from ..util import remote_info
from ..config import get_branch_url, get_stage_config, get as get_config

# Notification Services
notifiers = [slack, hipchat]


def send(notif_type, params):
    ''' Send deployment notifications. '''

    enabled_services = [s for s in notifiers if s.is_enabled()]

    # If notifiers aren't configured just skip it.
    if not enabled_services:
        return

    remote_info('Sending notifications')
    notif_params = extract_notification_params(params)

    for service in enabled_services:
        service.send(notif_type, **notif_params)


def extract_notification_params(params):
    ''' Extract parameters for notification. '''
    config = get_config()
    stage_config = get_stage_config(params['stage'])

    return dict(
        user=params['user'],
        branch=params['branch'],
        branch_url=get_branch_url(params['branch']),
        project_name=config['project_name'],
        project_description=config['project_description'],
        repository_url=config['repository_url'],
        server_name=params['stage'],
        public_url=stage_config['public_url'],
        host=stage_config['host']
    )
