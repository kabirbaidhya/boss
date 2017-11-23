'''
Module for slack API.
'''

import requests
from boss.config import get as _get_config
from boss.core.notification import (
    get_color,
    get_message,
    get_notification_params
)


def send(notif_type, **params):
    ''' Send slack notifications. '''
    notification = get_notification_params(
        create_link=create_link,
        **params
    )
    color = get_color(notif_type, config())
    text = get_message(notif_type, **notification)

    # Notify on slack
    notify({
        'attachments': [
            {
                'color': color,
                'text': text
            }
        ]
    })


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
