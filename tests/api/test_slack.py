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
def slack_url():
    return slack.slack_url(
        slack.config()['base_url'],
        slack.config()['endpoint']
    )


def test_create_link():
    ''' Test slack.create_link(). '''
    url = 'http://test-link-url'
    title = 'Test link'
    expected_link = '<{url}|{title}>'.format(url=url, title=title)
    assert slack.create_link(url, title) == expected_link


def test_create_link_supports_empty_url():
    ''' Test slack.create_link() supports empty url. '''
    assert slack.create_link(None, 'Test') == 'Test'


def test_slack_url():
    ''' Test slack_url() works. '''
    assert slack.slack_url('', '') == ''
    assert slack.slack_url(
        'https://hooks.slack.com/services',
        '/foo/bar'
    ) == 'https://hooks.slack.com/services/foo/bar'

    assert slack.slack_url(
        'https://hooks.slack.com/services',
        'https://hooks.slack.com/services/foo/bar'
    ) == 'https://hooks.slack.com/services/foo/bar'

    assert slack.slack_url(
        '',
        'https://hooks.slack.com/services/foo/bar'
    ) == 'https://hooks.slack.com/services/foo/bar'


def test_slack_url_with_no_leading_trailing_slashes():
    ''' Test no trailing or leading slashes are required. '''
    assert slack.slack_url(
        'https://hooks.slack.com/services',
        'just-test'
    ) == 'https://hooks.slack.com/services/just-test'


def test_send(slack_url):
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
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_send_deployment_started_with_no_repository_url(slack_url):
    ''' Test deployment started notification with no repository url. '''
    notify_params = dict(
        branch='temp',
        commit='tttt',
        commit_url=None,
        branch_url=None,
        repository_url=None,
        public_url='http://public-url',
        host='test-notify-deploying-host',
        project_name='project-name',
        server_name='server-name',
        server_link='http://server-link',
        user='user',
    )

    payload = {
        'attachments': [
            {
                'color': 'good',
                'text': 'user is deploying project-name:temp (tttt) to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_send_deployment_finished_with_no_repository_url(slack_url):
    ''' Test deployment finished notification with no repository url. '''
    notify_params = dict(
        branch='temp',
        commit='tttt',
        commit_url=None,
        branch_url=None,
        repository_url=None,
        public_url='http://public-url',
        host='test-notify-deploying-host',
        project_name='project-name',
        server_name='server-name',
        server_link='http://server-link',
        user='user',
    )

    payload = {
        'attachments': [
            {
                'color': '#764FA5',
                'text': 'user finished deploying project-name:temp (tttt) to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_send_with_no_branch_name(slack_url):
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
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deployed(slack_url):
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
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deployed_with_no_commit(slack_url):
    ''' Test sending deployment finished notification with no commit. '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='temp',
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
                'text': 'user finished deploying <http://repository-url|project-name>:<http://branch-url|temp> to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deploying_with_no_commit(slack_url):
    ''' Test sending deployment started notification with no commit. '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='temp',
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
                'color': 'good',
                'text': 'user is deploying <http://repository-url|project-name>:<http://branch-url|temp> to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deployed_with_no_branch_name(slack_url):
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
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deployment_finished_with_no_commit_no_branch(slack_url):
    ''' Test sending deployment finished notification with no commit and no branch. '''
    notify_params = dict(
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
                'text': 'user finished deploying <http://repository-url|project-name> to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deployment_started_with_no_commit_no_branch(slack_url):
    ''' Test sending deployment started notification with no commit and no branch. '''
    notify_params = dict(
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
                'color': 'good',
                'text': 'user is deploying <http://repository-url|project-name> to <http://public-url|server-name> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_notity_deployment_started_no_links_at_all(slack_url):
    ''' Test deployment started notification with no links or urls at all. '''
    notify_params = dict(
        project_name='project-name',
        server_name='staging',
        user='user',
    )

    payload = {
        'attachments': [
            {
                'color': 'good',
                'text': 'user is deploying project-name to staging server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_send_running_script_started_notification(slack_url):
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
                'text': 'user is running <http://repository-url|project-name>:migration on <http://public-url|stage> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(RUNNING_SCRIPT_STARTED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)


def test_send_running_script_finished_notification(slack_url):
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
                'text': 'user finished running <http://repository-url|project-name>:migration on <http://public-url|stage> server.',
                'mrkdwn_in': ['text']
            }
        ]
    }

    with patch('requests.post') as mock_post:
        slack.send(RUNNING_SCRIPT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(slack_url, json=payload)
