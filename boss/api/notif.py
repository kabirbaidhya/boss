'''
Notification API module.
'''

from ..util import remote_info
from . import slack, hipchat, git
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
    commit_url = git.get_commit_url(params['commit'], config['repository_url'])

    notif_params = dict(
        user=params['user'],
        commit_url=commit_url,
        commit=params['commit'],
        project_name=config['project_name'],
        project_description=config['project_description'],
        repository_url=config['repository_url'],
        server_name=params['stage'],
        public_url=stage_config['public_url'],
        host=stage_config['host']
    )

    # If branch is provided and branch is not HEAD, then add branch & branch_url.
    #
    # Note: While deploying from CI eg: Travis sometimes branch is not received
    # or is received as HEAD, which doesn't really make sense.
    # So, just hide the branch in those cases.
    if params.get('branch') and params.get('branch') != 'HEAD':
        notif_params['branch'] = params['branch']
        notif_params['branch_url'] = get_branch_url(params['branch'])

    return notif_params
