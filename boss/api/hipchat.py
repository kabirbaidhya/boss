'''
Module for hipchat API.
'''

import requests
from ..config import get as _get_config

from boss.core.ci import is_ci
from boss.constants import (
    NOTIFICATION_DEPLOYMENT_STARTED,
    NOTIFICATION_DEPLOYMENT_FINISHED
)

DEPLOYING_MESSAGE = '{user} is deploying {project_link} ({commit_link}) to {server_link} server.'
DEPLOYING_MESSAGE_WITH_BRANCH = '{user} is deploying {project_link}:{branch_link} ({commit_link}) to {server_link} server.'

DEPLOYED_SUCCESS_MESSAGE = '{user} finished deploying {project_link} ({commit_link}) to {server_link} server.'
DEPLOYED_SUCCESS_MESSAGE_WITH_BRANCH = '{user} finished deploying {project_link}:{branch_link} ({commit_link}) to {server_link} server.'


HIPCHAT_API_URL = 'https://{company_name}.hipchat.com/v2/room/{room_id}/notification?auth_token={auth_token}'


def send(notif_type, **params):
    '''
    Send hipchat notifications.
    '''
    handlers = {
        NOTIFICATION_DEPLOYMENT_STARTED: notify_deploying,
        NOTIFICATION_DEPLOYMENT_FINISHED: notify_deployed
    }

    handlers[notif_type](**params)


def config():
    ''' Get hipchat configuration. '''
    return _get_config()['notifications']['hipchat']


def is_enabled():
    ''' Check if hipchat is enabled or not. '''
    return config()['enabled']


def create_link(url, title):
    ''' Create a link for hipchat payload. '''
    markup = '<a href="{url}">{title}</a>'

    return markup.format(url=url, title=title)


def notify(payload):
    ''' Send a notification on hipchat. '''

    url = HIPCHAT_API_URL.format(
        company_name=config()['company_name'],
        room_id=config()['room_id'],
        auth_token=config()['auth_token']
    )
    requests.post(url, json=payload)


def get_notif_params(**params):
    ''' Get hipchat notification params. '''
    result = dict(
        user=params['user'],
        project_link=create_link(
            params['repository_url'],
            params['project_name']
        ),
        commit_link=create_link(
            params['commit_url'],
            params['commit']
        ),
        server_link=create_link(
            params['public_url'], params['server_name']
        )
    )

    if params.get('branch_url') and params.get('branch'):
        result['branch_link'] = create_link(
            params['branch_url'],
            params['branch']
        )

    return result


def notify_deploying(**params):
    ''' Send Deploying notification on Hipchat. '''
    notification = get_notif_params(**params)

    # If the branch is provided, display branch name in the message.
    if notification.has_key('branch_link'):
        text = DEPLOYING_MESSAGE_WITH_BRANCH.format(**notification)
    else:
        text = DEPLOYING_MESSAGE.format(**notification)

    if is_ci():
        color = config()['ci_deploying_color']
    else:
        color = config()['deploying_color']

    # Notify on hipchat
    notify({
        'color': color,
        'message': text,
        'notify': config()['notify'],
        'message_format': 'html'
    })


def notify_deployed(**params):
    ''' Send Deployed notification on Hipchat. '''
    notification = get_notif_params(**params)

    # If the branch is provided, display branch name in the message.
    if notification.has_key('branch_link'):
        text = DEPLOYED_SUCCESS_MESSAGE_WITH_BRANCH.format(**notification)
    else:
        text = DEPLOYED_SUCCESS_MESSAGE.format(**notification)

    if is_ci():
        color = config()['ci_deployed_color']
    else:
        color = config()['deployed_color']

    # Notify on hipchat
    notify({
        'color': color,
        'message': text,
        'notify': config()['notify'],
        'message_format': 'html'
    })
