''' Tests for boss.api.notif module. '''

from mock import patch

from boss.api import notif


@patch('boss.api.notif.remote_info')
@patch('boss.api.notif.get_config')
@patch('boss.api.notif.get_stage_config')
@patch('boss.api.slack.is_enabled')
@patch('boss.api.slack.notify_deploying')
def test_notif_sends_slack_notification(slack_notify_deploying_m, slack_is_enabled_m, gsc_m, get_m, _):
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

    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    slack_notify_deploying_m.assert_called_with(
        branch='my-branch',
        branch_url='/branch/my-branch',
        host='example.com',
        project_description='Just a test project',
        project_name='test-project',
        public_url='https://example.com',
        repository_url='https://github.com/kabirbaidhya/boss',
        server_name='test-server',
        user='ssh-user'
    )


@patch('boss.api.notif.remote_info')
@patch('boss.api.notif.get_config')
@patch('boss.api.notif.get_stage_config')
@patch('boss.api.hipchat.is_enabled')
@patch('boss.api.hipchat.notify_deploying')
def test_notif_sends_hipchat_notification(hipchat_notify_deploying_m, hipchat_is_enabled_m, gsc_m, get_m, _):
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

    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    hipchat_notify_deploying_m.assert_called_with(
        branch='my-branch',
        branch_url='/branch/my-branch',
        host='example.com',
        project_description='Just a test project',
        project_name='test-project',
        public_url='https://example.com',
        repository_url='https://github.com/kabirbaidhya/boss',
        server_name='test-server',
        user='ssh-user'
    )
