''' Tests for boss.core.ci module. '''

import os
from boss.core.ci import is_ci


def test_is_ci_returns_true_case_1():
    '''
    Test is_ci() returns True if CI=true,
    is passed through environment variables.
    '''
    os.environ['CI'] = 'true'

    assert is_ci() is True


def test_is_ci_returns_true_case_2():
    '''
    Test is_ci() returns True if CONTINUOUS_INTEGRATION=true,
    is passed through environment variables.
    '''
    os.environ['CONTINUOUS_INTEGRATION'] = 'true'

    assert is_ci() is True


def test_is_ci_returns_false():
    '''
    Test is_ci() returns True if CONTINUOUS_INTEGRATION=true,
    is passed through environment variables.
    '''
    os.environ['CI'] = ''
    os.environ['CONTINUOUS_INTEGRATION'] = ''

    assert is_ci() is False
