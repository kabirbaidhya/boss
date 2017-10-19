import unittest
from mock import patch

from boss.api.slack import config
from boss.api.slack import create_link
from boss.api.slack import notify
from boss.api.slack import notify_deploying


class TestBoseApiSlack(unittest.TestCase):
    def setUp(self):
        self.base_url = config()['base_url'] + config()['endpoint']

    def test_create_link(self):
        url = 'http://test-link-url'
        title = 'test link'
        expected_link = '<{url}|{title}>'.format(url=url, title=title)
        self.assertEqual(create_link(url, title), expected_link)

    def test_notify(self):
        with patch('requests.post') as mock_post:
            payload = {"message": "test message"}
            notify(payload)
            mock_post.assert_called_once_with(self.base_url, json=payload)

    def test_notity_deploying(self):
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
        with patch('requests.post') as mock_post:
            notify_deploying(**notify_params)
            mock_post.assert_called_once_with(self.base_url, json=payload)

    def test_notity_deployed(self):
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
        with patch('requests.post') as mock_post:
            notify_deploying(**notify_params)
            mock_post.assert_called_once_with(self.base_url, json=payload)
