'''
Module for slack API.
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


message_map = {
    NOTIFICATION_DEPLOYMENT_STARTED: {
        'message': DEPLOYING_MESSAGE,
        'message_with_branch': DEPLOYING_MESSAGE_WITH_BRANCH
    },
    NOTIFICATION_DEPLOYMENT_FINISHED: {
        'message': DEPLOYED_SUCCESS_MESSAGE,
        'message_with_branch': DEPLOYED_SUCCESS_MESSAGE_WITH_BRANCH
    },
}


def get_message(notif_type, **notification):
    # If the branch is provided, display branch name in the message.
    # TODO: CI link
    messages = message_map[notif_type]

    if notification.has_key('branch_link'):
        text = messages['message_with_branch'].format(**notification)
    else:
        text = messages['message'].format(**notification)

    return text


def send(notif_type, **params):
    '''
    Send slack notifications.
    '''
    handlers = {
        NOTIFICATION_DEPLOYMENT_STARTED: notify_deploying,
        NOTIFICATION_DEPLOYMENT_FINISHED: notify_deployed
    }

    handlers[notif_type](**params)


def config():
    ''' Get slack configuration. '''
    return _get_config()['notifications']['slack']


def is_enabled():
    ''' Check if slack is enabled or not. '''
    return config()['enabled']


def create_link(url, title):
    ''' Create a link for slack payload. '''
    return '<{url}|{title}>'.format(
        url=url,
        title=title
    )


def notify(payload):
    ''' Send a notification on Slack. '''
    url = config()['base_url'] + config()['endpoint']
    requests.post(url, json=payload)


def get_notif_params(**params):
    ''' Get slack notification params. '''
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
    ''' Send Deploying notification on Slack. '''

    notification = get_notif_params(**params)
    text = get_message(NOTIFICATION_DEPLOYMENT_STARTED, **notification)

    if is_ci():
        color = config()['ci_deploying_color']
    else:
        color = config()['deploying_color']

    # Notify on slack
    notify({
        'attachments': [
            {
                'color': color,
                'text': text
            }
        ]
    })


def notify_deployed(**params):
    ''' Send Deployed notification on Slack. '''

    notification = get_notif_params(**params)
    text = get_message(NOTIFICATION_DEPLOYMENT_FINISHED, **notification)

    if is_ci():
        color = config()['ci_deployed_color']
    else:
        color = config()['deployed_color']

    # Notify on slack
    notify({
        'attachments': [
            {
                'color': color,
                'text': text
            }
        ]
    })
