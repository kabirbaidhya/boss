'''
Notification API module.
'''

from . import slack
from . import hipchat
from ..config import get_branch_url, get_stage_config, get as get_config

DEPLOYMENT_STARTED = 1
DEPLOYMENT_FINISHED = 2


def send(notif_type, params):
    ''' Send deployment notifications. '''
    handlers = {
        DEPLOYMENT_STARTED: send_deploying_notification,
        DEPLOYMENT_FINISHED: send_deployed_notification
    }

    # Trigger the corresponding handler by notif_type.
    handlers[notif_type](params)


def send_deploying_notification(params):
    ''' Send deploying status notification. '''
    config = get_config()
    stage_config = get_stage_config(params['stage'])

    # Notify on slack
    if slack.is_enabled():
        slack.notify_deploying(
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

    # Notify on hipchat
    if hipchat.is_enabled():
        hipchat.notify_deploying(
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


def send_deployed_notification(params):
    ''' Send deployed finish status notification. '''
    config = get_config()
    stage_config = get_stage_config(params['stage'])

    # Notify on slack
    if slack.is_enabled():
        slack.notify_deployed(
            branch=params['branch'],
            branch_url=get_branch_url(params['branch']),
            project_name=config['project_name'],
            project_description=config['project_description'],
            repository_url=config['repository_url'],
            server_name=params['stage'],
            public_url=stage_config['public_url'],
            host=stage_config['host']
        )

    # Notify on hipchat
    if hipchat.is_enabled():
        hipchat.notify_deployed(
            branch=params['branch'],
            branch_url=get_branch_url(params['branch']),
            project_name=config['project_name'],
            project_description=config['project_description'],
            repository_url=config['repository_url'],
            server_name=params['stage'],
            public_url=stage_config['public_url'],
            host=stage_config['host']
        )

