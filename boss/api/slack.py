'''
Module for slack API.
'''

import requests
from boss.config import get as get_config
from boss.core import notification
from boss.core.util.func import as_is


def send(notif_type, **params):
    ''' Send slack notifications. '''
    url = slack_url(config()['base_url'], config()['endpoint'])

    (text, color) = notification.get(
        notif_type,
        config=get_config(),
        notif_config=config(),
        create_link=create_link,
        pre_format=as_is,
        **params
    )

    payload = {
        'attachments': [
            {
                'color': color,
                'text': text,
                'mrkdwn_in': ['text']
            }
        ]
    }

    requests.post(url, json=payload)


def config():
    ''' Get slack configuration. '''
    return get_config()['notifications']['slack']


def is_enabled():
    ''' Check if slack is enabled or not. '''
    return config()['enabled']


def create_link(url, title):
    ''' Create a link for slack payload. '''
    if not url:
        return title

    return '<{url}|{title}>'.format(
        url=url,
        title=title
    )


def slack_url(base_url, endpoint):
    ''' Return slack endpoint by concatinating the base_url if required '''
    base_url = base_url.strip('/')
    endpoint = endpoint.strip('/')

    if base_url in endpoint:
        return endpoint

    return base_url + '/' + endpoint


def pre_format(text):
    ''' Return pre-formatted text for slack. '''
    return '`{text}`'.format(text=text)
