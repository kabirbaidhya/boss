''' Tests for boss.api.notif module. '''

from mock import patch

from boss.api import notif
from boss.core.constants.notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED
)


@patch('boss.api.notif.get_config')
@patch('boss.api.notif.get_stage_config')
@patch('boss.api.slack.is_enabled')
@patch('boss.api.slack.send')
def test_notif_sends_slack_notification(slack_send_m, slack_is_enabled_m, gsc_m, get_m):
    ''' Test notif.send sends slack notification if slack is enabled. '''
    commit = 't12345'
    commit_url = 'https://github.com/kabirbaidhya/boss/tree/t12345'
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
    branch_url = 'https://github.com/kabirbaidhya/boss/tree/my-branch'

    # Trigger deployment started notification
    notif.send(DEPLOYMENT_STARTED, {
        'user': 'ssh-user',
        'commit': commit,
        'branch': 'my-branch',
        'stage': 'test-server'
    })

    # Trigger deployment finished notification with branch=HEAD
    notif.send(DEPLOYMENT_FINISHED, {
        'user': 'ssh-user',
        'commit': commit,
        'branch': 'HEAD',
        'stage': 'test-server'
    })

    (call1, call2) = slack_send_m.call_args_list

    assert call1[0][0] == DEPLOYMENT_STARTED
    assert call1[1]['branch'] == 'my-branch'
    assert call1[1]['commit'] == commit
    assert call1[1]['commit_url'] == commit_url
    assert call1[1]['branch_url'] == branch_url
    assert call1[1]['host'] == 'example.com'
    assert call1[1]['project_name'] == 'test-project'
    assert call1[1]['public_url'] == 'https://example.com'
    assert call1[1]['repository_url'] == 'https://github.com/kabirbaidhya/boss'
    assert call1[1]['server_name'] == 'test-server'
    assert call1[1]['user'] == 'ssh-user'

    assert call2[0][0] == DEPLOYMENT_FINISHED
    assert call2[1]['branch'] is None
    assert call2[1]['commit'] == commit
    assert call2[1]['commit_url'] == commit_url
    assert call2[1]['host'] == 'example.com'
    assert call2[1]['project_name'] == 'test-project'
    assert call2[1]['public_url'] == 'https://example.com'
    assert call2[1]['repository_url'] == 'https://github.com/kabirbaidhya/boss'
    assert call2[1]['server_name'] == 'test-server'
    assert call2[1]['user'] == 'ssh-user'
