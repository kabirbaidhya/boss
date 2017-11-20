'''
Notification API module.
'''

from . import slack
from . import hipchat
from ..util import remote_info
from ..config import get_branch_url, get_stage_config, get as get_config

DEPLOYMENT_STARTED = 1
DEPLOYMENT_FINISHED = 2


def send(notif_type, params):
    ''' Send deployment notifications. '''
    handlers = {
        DEPLOYMENT_STARTED: send_deploying_notification,
        DEPLOYMENT_FINISHED: send_deployed_notification
    }

    # If notifications are enabled then, print a message (Info).
    if slack.is_enabled() or hipchat.is_enabled():
        remote_info('Sending notifications')

    # Trigger the corresponding handler by notif_type.
    handlers[notif_type](params)


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


def send_deploying_notification(params):
    ''' Send deploying status notification. '''
    notif_params = extract_notification_params(params)

    # Notify on slack
    if slack.is_enabled():
        slack.notify_deploying(**notif_params)

    # Notify on hipchat
    if hipchat.is_enabled():
        hipchat.notify_deploying(**notif_params)


def send_deployed_notification(params):
    ''' Send deployed finish status notification. '''
    notif_params = extract_notification_params(params)

    # Notify on slack
    if slack.is_enabled():
        slack.notify_deployed(**notif_params)

    # Notify on hipchat
    if hipchat.is_enabled():
        hipchat.notify_deployed(**notif_params)
