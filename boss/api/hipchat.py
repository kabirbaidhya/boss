'''
Module for hipchat API.
'''

import json
import requests
from fabric.api import local, parallel
from ..config import get as _get_config

DEPLOYING_MESSAGE = '{user} is deploying {project_link}:{branch_link} to {server_link} server.'
DEPLOYED_SUCCESS_MESSAGE = 'Finished deploying {project_link}:{branch_link} to {server_link} server.'


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


@parallel
def notify(payload):
    ''' Send a notification on hipchat. '''

    url = 'https://{company_name}.hipchat.com/v2/room/{room_id}/notification?auth_token={auth_token}'.format(
        company_name=config()['company_name'],
        room_id=config()['room_id'],
        auth_token=config()['auth_token']
    )
    requests.post(url, json=payload)


def notify_deploying(**params):
    ''' Send Deploying notification on Hipchat. '''
    branch_link = create_link(params['branch_url'], params['branch'])
    server_link = create_link(params['public_url'], params['host'])
    project_link = create_link(
        params['repository_url'],
        params['project_name']
    )

    server_short_link = create_link(
        params['public_url'], params['server_name']
    )

    text = DEPLOYING_MESSAGE.format(
        user=params['user'],
        branch_link=branch_link,
        project_link=project_link,
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
    branch_link = create_link(params['branch_url'], params['branch'])
    server_link = create_link(params['public_url'], params['host'])
    server_short_link = create_link(
        params['public_url'],
        params['server_name']
    )
    project_link = create_link(
        params['repository_url'],
        params['project_name']
    )

    text = DEPLOYED_SUCCESS_MESSAGE.format(
        branch_link=branch_link,
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
