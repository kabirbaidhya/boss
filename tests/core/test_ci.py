''' Tests for boss.core.ci module. '''

import os
from boss.core.ci import (
    is_ci,
    is_travis,
    get_ci_link
)
from boss.core.constants.config import DEFAULT_CONFIG


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


def test_is_travis_returns_true_for_travis_ci():
    ''' Test is_travis() returns True for Travis CI. '''
    os.environ['CI'] = 'true'
    os.environ['BOSS_RUNNING'] = 'true'
    os.environ['TRAVIS'] = 'true'

    assert is_travis() is True


def test_get_ci_link_returns_travis_link_for_travis_ci_for_default_config():
    ''' Test travis build link is returned for travis ci. '''
    os.environ['CI'] = 'true'
    os.environ['BOSS_RUNNING'] = 'true'
    os.environ['TRAVIS'] = 'true'
    os.environ['TRAVIS_BUILD_ID'] = '59945015'
    os.environ['TRAVIS_REPO_SLUG'] = 'test/test'

    config = DEFAULT_CONFIG
    params = {}
    expected_link = 'https://travis-ci.com/test/test/builds/59945015'

    assert get_ci_link(config) == expected_link


def test_get_ci_link_returns_travis_link_for_travis_ci_for_configured_base_url():
    '''
    Test travis build link is returned for travis ci
    with configured base_url with or without (trailing slash).
    '''
    os.environ['CI'] = 'true'
    os.environ['BOSS_RUNNING'] = 'true'
    os.environ['TRAVIS'] = 'true'
    os.environ['TRAVIS_BUILD_ID'] = '59945015'
    os.environ['TRAVIS_REPO_SLUG'] = 'test/test'

    # base_url (regular)
    config1 = {
        'ci': {
            'base_url': 'https://travis-ci.org'
        }
    }
    # base_url (with trailing slash)
    config2 = {
        'ci': {
            'base_url': 'https://travis-ci.org/'
        }
    }
    expected_link = 'https://travis-ci.org/test/test/builds/59945015'

    assert get_ci_link(config1) == expected_link
    assert get_ci_link(config2) == expected_link


def test_get_ci_link_returns_none_for_unknown_ci_providers_under_default_config():
    ''' Test get_ci_link() returns None for unknown CI providers. '''
    os.environ['CI'] = 'true'
    os.environ['BOSS_RUNNING'] = 'true'
    os.environ['TRAVIS'] = ''  # Unset TRAVIS (if it's set)

    assert get_ci_link(DEFAULT_CONFIG) is None
