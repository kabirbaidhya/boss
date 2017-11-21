''' Tests for boss.core.ci module. '''

import os
from boss.core.ci import is_ci


def test_is_ci_returns_true_case_1():
    '''
    Test is_ci() returns True if CI=true,
    is passed through environment variables.
    '''
    os.environ['BOSS_RUNNING'] = 'true'
    os.environ['CI'] = 'true'

    assert is_ci() is True


def test_is_ci_returns_true_case_2():
    '''
    Test is_ci() returns True if CONTINUOUS_INTEGRATION=true,
    is passed through environment variables.
    '''
    os.environ['BOSS_RUNNING'] = 'true'
    os.environ['CONTINUOUS_INTEGRATION'] = 'true'

    assert is_ci() is True


def test_is_ci_returns_false():
    '''
    Test is_ci() returns False if CI related environment variables,
    are not found.
    '''
    os.environ['CI'] = ''
    os.environ['CONTINUOUS_INTEGRATION'] = ''

    assert is_ci() is False


def test_is_ci_returns_false_if_boss_is_not_running_in_run_mode():
    '''
    Test is_ci() returns False if boss is not running (test environment).
    (This is to check is_ci() function works well when these tests are running in CI).
    '''
    os.environ['BOSS_RUNNING'] = ''
    os.environ['CI'] = 'true'
    os.environ['CONTINUOUS_INTEGRATION'] = 'true'

    assert is_ci() is False
