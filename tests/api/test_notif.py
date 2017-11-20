''' Tests for boss.api.notif module. '''

from mock import patch, call

from boss.api import notif
from boss.constants import (
    NOTIFICATION_DEPLOYMENT_STARTED,
    NOTIFICATION_DEPLOYMENT_FINISHED
)


@patch('boss.api.notif.remote_info')
@patch('boss.api.notif.get_config')
@patch('boss.api.notif.get_stage_config')
@patch('boss.api.slack.is_enabled')
@patch('boss.api.slack.send')
def test_notif_sends_slack_notification(slack_send_m, slack_is_enabled_m, gsc_m, get_m, _):
    ''' Test notif.send sends slack notification if slack is enabled. '''

    get_m.return_value = {
        'project_name': 'test-project',
        'project_description': 'Just a test project',
        'repository_url': 'https://github.com/kabirbaidhya/boss',
    }
    gsc_m.return_value = {
        'public_url': 'https://example.com',
        'host': 'example.com'
    }
    slack_is_enabled_m.return_value = True

    # Trigger deployment started notification
    notif.send(NOTIFICATION_DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    # Trigger Deployment finished notification
    notif.send(NOTIFICATION_DEPLOYMENT_FINISHED, {
        'user': 'ssh-user',
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    # Trigger deployment started notification with branch=HEAD
    notif.send(NOTIFICATION_DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'branch': 'HEAD',
        'stage': 'test-server'
    })

    # Trigger deployment started notification with no branch
    notif.send(NOTIFICATION_DEPLOYMENT_FINISHED, {
        'user': 'ssh-user',
        'stage': 'test-server'
    })

    slack_send_m.assert_has_calls([
        call(
            NOTIFICATION_DEPLOYMENT_STARTED,
            branch='my-branch',
            branch_url='/branch/my-branch',
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        ),
        call(
            NOTIFICATION_DEPLOYMENT_FINISHED,
            branch='my-branch',
            branch_url='/branch/my-branch',
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        ),
        call(
            NOTIFICATION_DEPLOYMENT_STARTED,
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        ),
        call(
            NOTIFICATION_DEPLOYMENT_FINISHED,
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        )
    ])


@patch('boss.api.notif.remote_info')
@patch('boss.api.notif.get_config')
@patch('boss.api.notif.get_stage_config')
@patch('boss.api.hipchat.is_enabled')
@patch('boss.api.hipchat.send')
def test_notif_sends_hipchat_notification(hipchat_send_m, hipchat_is_enabled_m, gsc_m, get_m, _):
    ''' Test notif.send sends hipchat notification if hipchat is enabled. '''

    get_m.return_value = {
        'project_name': 'test-project',
        'project_description': 'Just a test project',
        'repository_url': 'https://github.com/kabirbaidhya/boss',
    }
    gsc_m.return_value = {
        'public_url': 'https://example.com',
        'host': 'example.com'
    }
    hipchat_is_enabled_m.return_value = True

    # Trigger deployment started notification
    notif.send(NOTIFICATION_DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    # Trigger deployment finished notification
    notif.send(NOTIFICATION_DEPLOYMENT_FINISHED, {
        'user': 'ssh-user',
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    # Trigger Deployment Started notification with branch=HEAD
    notif.send(NOTIFICATION_DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'branch': 'HEAD',
        'stage': 'test-server'
    })

    # Trigger Deployment Started notification with no branch
    notif.send(NOTIFICATION_DEPLOYMENT_FINISHED, {
        'user': 'ssh-user',
        'stage': 'test-server'
    })

    hipchat_send_m.assert_has_calls([
        call(
            NOTIFICATION_DEPLOYMENT_STARTED,
            branch='my-branch',
            branch_url='/branch/my-branch',
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        ),
        call(
            NOTIFICATION_DEPLOYMENT_FINISHED,
            branch='my-branch',
            branch_url='/branch/my-branch',
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        ),
        call(
            NOTIFICATION_DEPLOYMENT_STARTED,
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        ),
        call(
            NOTIFICATION_DEPLOYMENT_FINISHED,
            host='example.com',
            project_description='Just a test project',
            project_name='test-project',
            public_url='https://example.com',
            repository_url='https://github.com/kabirbaidhya/boss',
            server_name='test-server',
            user='ssh-user'
        )
    ])
