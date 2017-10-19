import unittest

from boss.api.slack import create_link


class TestBoseApiSlack(unittest.TestCase):
    def test_create_link(self):
        url = 'http://test-link-url'
        title = 'test link'
        expected_link = '<{url}|{title}>'.format(url=url, title=title)
        self.assertEqual(create_link(url, title), expected_link)
