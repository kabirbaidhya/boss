import unittest
from mock import patch

from boss.api.slack import config
from boss.api.slack import create_link
from boss.api.slack import notify


class TestBoseApiSlack(unittest.TestCase):
    def test_create_link(self):
        url = 'http://test-link-url'
        title = 'test link'
        expected_link = '<{url}|{title}>'.format(url=url, title=title)
        self.assertEqual(create_link(url, title), expected_link)

    def test_notify(self):
        with patch('requests.post') as mock_post:
            base_url = config()['base_url'] + config()['endpoint']
            payload = {"message": "test message"}
            notify(payload)
            mock_post.assert_called_once_with(base_url, json=payload)
