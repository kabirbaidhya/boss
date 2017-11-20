'''
Module for slack API.
'''


import requests
from ..config import get as _get_config

DEPLOYING_MESSAGE = '{user} is deploying {project_link} to {server_link} server.'
DEPLOYING_MESSAGE_WITH_BRANCH = '{user} is deploying {project_link}:{branch_link} to {server_link} server.'

DEPLOYED_SUCCESS_MESSAGE = '{user} finished deploying {project_link} to {server_link} server.'
DEPLOYED_SUCCESS_MESSAGE_WITH_BRANCH = '{user} finished deploying {project_link}:{branch_link} to {server_link} server.'


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


def notify_deploying(**params):
    ''' Send Deploying notification on Slack. '''

    project_link = create_link(
        params['repository_url'],
        params['project_name']
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
            project_link=project_link,
            server_link=server_short_link
        )
    else:
        text = DEPLOYING_MESSAGE.format(
            user=params['user'],
            project_link=project_link,
            server_link=server_short_link
        )

    payload = {
        'attachments': [
            {
                'color': config()['deploying_color'],
                'text': text
            }
        ]
    }

    # Notify on slack
    notify(payload)


def notify_deployed(**params):
    ''' Send Deployed notification on Slack. '''

    server_short_link = create_link(
        params['public_url'],
        params['server_name']
    )
    project_link = create_link(
        params['repository_url'],
        params['project_name']
    )

    if params.get('branch_url') and params.get('branch'):
        branch_link = create_link(params['branch_url'], params['branch'])
        text = DEPLOYED_SUCCESS_MESSAGE_WITH_BRANCH.format(
            user=params['user'],
            branch_link=branch_link,
            project_link=project_link,
            server_link=server_short_link
        )
    else:
        text = DEPLOYED_SUCCESS_MESSAGE.format(
            user=params['user'],
            project_link=project_link,
            server_link=server_short_link
        )

    payload = {
        'attachments': [
            {
                'color': config()['deployed_color'],
                'text': text
            }
        ]
    }

    # Notify on slack
    notify(payload)
