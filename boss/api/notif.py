'''
Notification API module.
'''

from boss.core.output import warn
from boss.api import slack, hipchat, git
from boss.config import get_stage_config, get as get_config

# Notification Services
notifiers = [slack, hipchat]


def send(notif_type, params):
    ''' Send deployment notifications. '''

    enabled_services = [s for s in notifiers if s.is_enabled()]

    # If notifiers aren't configured just skip it.
    if not enabled_services:
        return

    notif_params = extract_notification_params(params)

    try:
        for service in enabled_services:
            service.send(notif_type, **notif_params)
    except:
        # Should still proceed if error sending notification,
        # printing an warning message.
        warn('Warning: Failed sending notifications.')


def extract_notification_params(params):
    ''' Extract parameters for notification. '''
    config = get_config()
    stage_config = get_stage_config(params['stage'])

    notif_params = dict(
        host=stage_config['host'],
        server_name=params['stage'],
        public_url=stage_config['public_url'],
        repository_url=config['repository_url'],
        project_name=config['project_name'],
        project_description=config['project_description'],
        **params
    )

    # If commit is provided, send commit_url too.
    if params.get('commit'):
        notif_params['commit_url'] = git.get_tree_url(
            params['commit'],
            config['repository_url']
        )

    # If branch is provided and branch is not HEAD, then add branch & branch_url.
    #
    # Note: While deploying from CI eg: Travis sometimes branch is not received
    # or is received as HEAD, which doesn't really make sense.
    # So, just hide the branch in those cases.
    if params.get('branch') and params.get('branch') != 'HEAD':
        notif_params['branch'] = params['branch']
        notif_params['branch_url'] = git.get_tree_url(
            params['branch'],
            config['repository_url']
        )
    else:
        notif_params['branch'] = None

    return notif_params
