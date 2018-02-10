# -*- coding: utf-8 -*-
''' Notification module. '''

from boss.core.ci import is_ci, get_ci_link
from boss.core.constants.notification import MESSAGE_MAP

CI_TEXT = 'CI'
CI_SEPARATOR = ' · '


def get(notif_type, **params):
    ''' Get notification. '''
    notification = get_notification_params(**params)
    color = get_color(notif_type, params['notif_config'])
    text = get_ci_prefix(**params) + get_message(notif_type, **notification)

    return (text, color)


def get_ci_prefix(**params):
    '''
    Return a CI prefix with CI build like on the notification,
    if running under CI environment.
    '''

    if not is_ci():
        return ''

    ci_url = get_ci_link(params['config'])
    create_link = params['create_link']

    if ci_url:
        return create_link(ci_url, CI_TEXT) + CI_SEPARATOR
    else:
        return CI_TEXT + CI_SEPARATOR


def get_message(notif_type, **notification):
    '''
    Get the notification message.
    If the branch is provided, display branch name in the message.
    '''

    messages = MESSAGE_MAP[notif_type]

    if notification.has_key('branch_link') and notification.has_key('commit_link'):
        text = messages['message_full'].format(**notification)
    elif notification.has_key('branch_link'):
        text = messages['message_with_branch'].format(**notification)
    elif notification.has_key('commit_link'):
        text = messages['message_with_commit'].format(**notification)
    else:
        text = messages['message'].format(**notification)

    return text


def get_color(notif_type, config):
    ''' Get color for notification. '''
    key = MESSAGE_MAP[notif_type]['color']
    ci_key = MESSAGE_MAP[notif_type]['ci_color']

    return config[ci_key] if is_ci() else config[key]


def get_notification_params(**params):
    ''' Get notification params from raw parameters. '''
    create_link = params['create_link']
    result = dict(user=params['user'])

    result['project_link'] = create_link(
        params.get('repository_url'),
        params['project_name']
    )

    if params.get('server_name'):
        result['server_link'] = create_link(
            params.get('public_url'),
            params['server_name']
        )

    if params.get('commit'):
        result['commit_link'] = create_link(
            params.get('commit_url'),
            params['commit']
        )

    if params.get('branch'):
        result['branch_link'] = create_link(
            params.get('branch_url'),
            params['branch']
        )

    if params.get('script'):
        preformat = params.get('pre_format') or (lambda x: x)
        result['script'] = preformat(params['script'])

    return result
