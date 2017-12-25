''' Tests for boss.api.slack module. '''

from mock import patch
from pytest import fixture
from boss.api import slack
from boss.core.constants.notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED,
    RUNNING_SCRIPT_STARTED,
    RUNNING_SCRIPT_FINISHED
)


@fixture(scope='function')
def base_url():
    return slack.config()['base_url'] + slack.config()['endpoint']


def test_create_link():
    ''' Test slack.create_link(). '''
    url = 'http://test-link-url'
    title = 'Test link'
    expected_link = '<{url}|{title}>'.format(url=url, title=title)
    assert slack.create_link(url, title) == expected_link


def test_send(base_url):
    ''' Test slack.send(). '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='temp',
        commit='tttt',
        commit_url='http://commit-url',
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='server-name',
        server_link='http://server-link',
        user='user',
    )

    payload = {
        'attachments': [
            {
                'color': 'good',
                'text': 'user is deploying <http://repository-url|project-name>:<http://branch-url|temp> (<http://commit-url|tttt>) to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_send_with_no_branch_name(base_url):
    '''
    Test slack.send() doesn't show the branch link,
    if branch name is not provided.
    '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        commit='tttt',
        commit_url='http://commit-url',
        project_name='project-name',
        server_name='server-name',
        server_link='http://server-link',
        user='user',
    )

    payload = {
        'attachments': [
            {
                'color': 'good',
                'text': 'user is deploying <http://repository-url|project-name> (<http://commit-url|tttt>) to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deployed(base_url):
    ''' Test slack.notify_deployed(). '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='temp',
        commit='tttt',
        commit_url='http://commit-url',
        public_url='http://public-url',
        host='test-notify-deployed-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='server-name',
        server_link='http://server-link',
        user='user'
    )
    payload = {
        'attachments': [
            {
                'color': '#764FA5',
                'text': 'user finished deploying <http://repository-url|project-name>:<http://branch-url|temp> (<http://commit-url|tttt>) to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deployed_with_no_branch_name(base_url):
    '''
    Test slack.notify_deployed() doesn't show the branch link,
    if branch name is not provided.
    '''

    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deployed-host',
        commit='tttt',
        commit_url='http://commit-url',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='server-name',
        server_link='http://server-link',
        user='user'
    )
    payload = {
        'attachments': [
            {
                'color': '#764FA5',
                'text': 'user finished deploying <http://repository-url|project-name> (<http://commit-url|tttt>) to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_send_running_script_started_notification(base_url):
    ''' Test send() sends RUNNING_SCRIPT_STARTED notfication. '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        script='migration',
        user='user'
    )

    payload = {
        'attachments': [
            {
                'color': 'good',
                'text': 'user is running `migration` for <http://repository-url|project-name> on <http://public-url|stage> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(RUNNING_SCRIPT_STARTED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_send_running_script_finished_notification(base_url):
    ''' Test send() sends RUNNING_SCRIPT_FINISHED notfication. '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        script='migration',
        user='user'
    )

    payload = {
        'attachments': [
            {
                'color': '#764FA5',
                'text': 'user finished running `migration` for <http://repository-url|project-name> on <http://public-url|stage> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(RUNNING_SCRIPT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)
