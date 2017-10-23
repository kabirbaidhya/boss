''' Tests for boss.api.slack module. '''

from mock import patch
from boss.api import slack


def test_create_link():
    ''' Test slack.create_link(). '''
    url = 'http://test-link-url'
    title = 'Test link'
    expected_link = '<{url}|{title}>'.format(url=url, title=title)
    assert slack.create_link(url, title) == expected_link


def test_notify():
    ''' Test slack.notify(). '''
    base_url = slack.config()['base_url'] + slack.config()['endpoint']

    with patch('requests.post') as mock_post:
        payload = {"message": "Test message"}
        slack.notify(payload)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deploying():
    ''' Test slack.notify_deploying(). '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='test_notify_deploying',
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='server-name',
        user='user',
    )
    payload = {
        "text": "user is deploying <http://repository-url|project-name>:<http://branch-url|test_notify_deploying> to <http://public-url|server-name> server.",
        "attachments": [
            {
                "color": "good",
                "fields": [
                    {
                        "short": True,
                        "value": "<http://branch-url|test_notify_deploying>",
                        "title": "Branch"
                    },
                    {
                        "short": True,
                        "value": "<http://public-url|test-notify-deploying-host>",
                        "title": "To"
                    }
                ],
                "title": "Deploying"
            }
        ]
    }
    base_url = slack.config()['base_url'] + slack.config()['endpoint']
    with patch('requests.post') as mock_post:
        slack.notify_deploying(**notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deployed():
    ''' Test slack.notify_deployed(). '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='test_notify_deployed',
        public_url='http://public-url',
        host='test-notify-deployed-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='server-name',
        user='user',
    )
    payload = {
        "text": "user is deploying <http://repository-url|project-name>:<http://branch-url|test_notify_deployed> to <http://public-url|server-name> server.",
        "attachments": [
            {
                "color": "good",
                "fields": [
                    {
                        "short": True,
                        "value": "<http://branch-url|test_notify_deployed>",
                        "title": "Branch"
                    },
                    {
                        "short": True,
                        "value": "<http://public-url|test-notify-deployed-host>",
                        "title": "To"
                    }
                ],
                "title": "Deploying"
            }
        ]
    }
    base_url = slack.config()['base_url'] + slack.config()['endpoint']

    with patch('requests.post') as mock_post:
        slack.notify_deploying(**notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)
