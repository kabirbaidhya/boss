'''
Module for hipchat API.
'''

import requests
from ..config import get as _get_config

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


def notify_deploying(**params):
    ''' Send Deploying notification on Hipchat. '''

    project_link = create_link(
        params['repository_url'],
        params['project_name']
    )
    commit_link = create_link(
        params['commit_url'],
        params['commit']
    )
    server_short_link = create_link(
        params['public_url'], params['server_name']
    )

    # If the branch is provided, display branch name in the message.
    if params.get('branch_url') and params.get('branch'):
        branch_link = create_link(params['branch_url'], params['branch'])
        text = DEPLOYING_MESSAGE_WITH_BRANCH.format(
            user=params['user'],
            branch_link=branch_link,
            commit_link=commit_link,
            project_link=project_link,
            server_link=server_short_link
        )
    else:
        text = DEPLOYING_MESSAGE.format(
            user=params['user'],
            project_link=project_link,
            commit_link=commit_link,
            server_link=server_short_link
        )

    payload = {
        'color': config()['deploying_color'],
        'message': text,
        'notify': config()['notify'],
        'message_format': 'html'
    }

    # Notify on hipchat
    notify(payload)


def notify_deployed(**params):
    ''' Send Deployed notification on Hipchat. '''
    server_short_link = create_link(
        params['public_url'],
        params['server_name']
    )
    commit_link = create_link(
        params['commit_url'],
        params['commit']
    )
    project_link = create_link(
        params['repository_url'],
        params['project_name']
    )

    # If the branch is provided, display branch name in the message.
    if params.get('branch_url') and params.get('branch'):
        branch_link = create_link(params['branch_url'], params['branch'])
        text = DEPLOYED_SUCCESS_MESSAGE_WITH_BRANCH.format(
            user=params['user'],
            branch_link=branch_link,
            commit_link=commit_link,
            project_link=project_link,
            server_link=server_short_link
        )
    else:
        text = DEPLOYED_SUCCESS_MESSAGE.format(
            user=params['user'],
            commit_link=commit_link,
            project_link=project_link,
            server_link=server_short_link
        )

    payload = {
        'color': config()['deployed_color'],
        'message': text,
        'notify': config()['notify'],
        'message_format': 'html'
    }

    # Notify on hipchat
    notify(payload)
