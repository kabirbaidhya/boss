import json
from boss import config
from fabric.api import local
from .util import get_user, get_branch_url

DEPLOYING_COLOR = 'good'
DEPLOYED_COLOR = '#764FA5'
HOOK_BASE_URI = 'https://hooks.slack.com/services'
DEPLOYING_MESSAGE = '{user} is deploying branch {branch_link} to {server_link} server.'
DEPLOYED_SUCCESS_MESSAGE = 'Finished deploying branch {branch_link} to {server_link} server.'


def is_enabled():
    return config['services']['slack']['enabled']


def notify(payload):
    command = 'curl -X POST -H "Content-type: application/json" --data \'%s\' %s'
    slack_url = HOOK_BASE_URI + config['services']['slack']['endpoint']

    # TODO: Do builtin functions for invoking the shell command
    local(command % (json.dumps(payload), slack_url))


def notify_deploying(**params):
    branch_url = get_branch_url(params['branch'])
    branch_link = create_link(branch_url, params['branch'])
    server_link = create_link(params['public_url'], params['host'])
    server_short_link = create_link(
        params['public_url'], params['server_name'])

    text = DEPLOYING_MESSAGE.format(
        user=get_user(),
        branch_link=branch_link,
        server_link=server_short_link)

    payload = {
        "text": text,
        "attachments": [
            {
                "title": "Deploying",
                "color": DEPLOYING_COLOR,
                "fields": [
                    {
                        "title": "Branch",
                        "value": branch_link,
                        "short": True
                    },
                    {
                        "title": "To",
                        "value": server_link,
                        "short": True
                    }
                ]
            }
        ]
    }

    # Notify on slack
    notify(payload)


def notify_deployed(**params):
    branch_url = get_branch_url(params['branch'])
    branch_link = create_link(branch_url, params['branch'])
    server_link = create_link(params['public_url'], params['host'])
    server_short_link = create_link(
        params['public_url'], params['server_name'])

    text = DEPLOYED_SUCCESS_MESSAGE.format(
        branch_link=branch_link,
        server_link=server_short_link)

    payload = {
        "text": text,
        "attachments": [
            {
                "title": "Finished Deploying",
                "color": DEPLOYED_COLOR,
                "fields": [
                    {
                        "title": "Branch",
                        "value": branch_link,
                        "short": True
                    },
                    {
                        "title": "To",
                        "value": server_link,
                        "short": True
                    }
                ]
            }
        ]
    }

    # Notify on slack
    notify(payload)


def create_link(url, title):
    return '<%s|%s>' % (url, title)
