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
        payload = {'message': 'Test message'}
        slack.notify(payload)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deploying():
    ''' Test slack.notify_deploying(). '''
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
                'text': 'user is deploying <http://repository-url|project-name>:<http://branch-url|temp> (<http://commit-url|tttt>) to <http://public-url|server-name> server.'
            }
        ]
    }
    base_url = slack.config()['base_url'] + slack.config()['endpoint']
    with patch('requests.post') as mock_post:
        slack.notify_deploying(**notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deploying_with_no_branch_name():
    '''
    Test slack.notify_deploying() doesn't show the branch link,
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
                'text': 'user is deploying <http://repository-url|project-name> (<http://commit-url|tttt>) to <http://public-url|server-name> server.'
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
                'text': 'user finished deploying <http://repository-url|project-name>:<http://branch-url|temp> (<http://commit-url|tttt>) to <http://public-url|server-name> server.'
            }
        ]
    }
    base_url = slack.config()['base_url'] + slack.config()['endpoint']

    with patch('requests.post') as mock_post:
        slack.notify_deployed(**notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deployed_with_no_branch_name():
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
                'text': 'user finished deploying <http://repository-url|project-name> (<http://commit-url|tttt>) to <http://public-url|server-name> server.'
            }
        ]
    }
    base_url = slack.config()['base_url'] + slack.config()['endpoint']

    with patch('requests.post') as mock_post:
        slack.notify_deployed(**notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)
