''' Notification module. '''

from boss.core.ci import is_ci
from boss.core.constants.notification import MESSAGE_MAP


def get_message(notif_type, **notification):
    # If the branch is provided, display branch name in the message.
    # TODO: CI link
    messages = MESSAGE_MAP[notif_type]

    if notification.has_key('branch_link'):
        text = messages['message_with_branch'].format(**notification)
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
