'''
Module for slack API.
'''

import requests
from boss.config import get as get_config
from boss.core import notification


def send(notif_type, **params):
    ''' Send slack notifications. '''
    url = config()['base_url'] + config()['endpoint']

    (text, color) = notification.get(
        notif_type,
        config=get_config(),
        notif_config=config(),
        create_link=create_link,
        pre_format=pre_format,
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
    return '<{url}|{title}>'.format(
        url=url,
        title=title
    )


def pre_format(text):
    ''' Return pre-formatted text for slack. '''
    return '`{text}`'.format(text=text)
