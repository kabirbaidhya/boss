''' Tests for runner. '''

from mock import patch

from boss.api.runner import should_notify, run_script
from boss.core.constants.notification_types import (
    RUNNING_SCRIPT_STARTED,
    RUNNING_SCRIPT_FINISHED
)


@patch('boss.api.runner._get_config')
def test_should_notify_if_all_scripts_are_to_be_notified(gc_m):
    ''' Test should_notify() returns True if all scripts are set to be notified. '''
    gc_m.return_value = {
        'notified_hooks': {
            'scripts': 'all'
        }
    }

    result = should_notify('foo')

    assert result is True


@patch('boss.api.runner._get_config')
def test_should_notify_if_provided_script_is_to_be_notified(gc_m):
    ''' Test should_notify() returns True if the provided script is to be notified. '''
    gc_m.return_value = {
        'notified_hooks': {
            'scripts': ['bar', 'foo', 'test']
        }
    }

    result = should_notify('foo')

    assert result is True


@patch('boss.api.runner._get_config')
def test_should_notify_returns_false(gc_m):
    ''' Test should_notify() returns False if it's not configured to be notifed. '''
    gc_m.return_value = {
        'notified_hooks': {
            'scripts': []
        }
    }

    assert not should_notify('foo')
    assert not should_notify('bar')


@patch('boss.api.runner._run')
@patch('boss.api.runner.hide')
@patch('boss.api.runner.host_info')
@patch('boss.api.runner._get_config')
@patch('boss.api.runner.notif.send')
@patch('boss.api.runner.shell.get_user')
@patch('boss.api.runner.shell.get_stage')
def test_run_script_send_script_running_notifications(gs_m, gu_m, send_m, gc_m, hi_m, h_m, r_m):
    gs_m.return_value = 'prod'
    gu_m.return_value = 'kabir'
    gc_m.return_value = {
        'scripts': {
            'foo': 'just foo'
        },
        'notified_hooks': {
            'scripts': ['foo']
        }
    }

    run_script('foo')

    send_m.assert_called()
    (call1, call2) = send_m.call_args_list

    assert call1[0][0] == RUNNING_SCRIPT_STARTED
    assert call1[0][1]['script'] == 'foo'
    assert call1[0][1]['user'] == 'kabir'
    assert call1[0][1]['stage'] == 'prod'

    assert call2[0][0] == RUNNING_SCRIPT_FINISHED
    assert call2[0][1]['script'] == 'foo'
    assert call2[0][1]['user'] == 'kabir'
    assert call2[0][1]['stage'] == 'prod'
