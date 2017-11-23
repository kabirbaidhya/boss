'''
Module for hipchat API.
'''

import requests
from ..config import get as _get_config
from boss.core.notification import (
    get_color,
    get_message,
    get_notification_params
)


API_BASE_URL = 'https://{company_name}.hipchat.com/v2/room/{room_id}/notification?auth_token={auth_token}'


def send(notif_type, **params):
    ''' Send hipchat notifications. '''
    notification = get_notification_params(
        create_link=create_link,
        **params
    )
    color = get_color(notif_type, config())
    text = get_message(notif_type, **notification)

    # Notify on hipchat
    notify({
        'color': color,
        'message': text,
        'notify': config()['notify'],
        'message_format': 'html'
    })


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

    url = API_BASE_URL.format(
        company_name=config()['company_name'],
        room_id=config()['room_id'],
        auth_token=config()['auth_token']
    )
    requests.post(url, json=payload)
