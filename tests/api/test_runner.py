''' Tests for runner. '''

from mock import patch

from boss.api.runner import should_notify


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
