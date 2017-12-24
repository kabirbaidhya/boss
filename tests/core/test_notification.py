# -*- coding: utf-8 -*-
''' Test boss.core.notification. '''

from mock import patch
from os import environ as env
from boss.core.constants.config import DEFAULT_CONFIG
from boss.core.constants.notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED
)
from boss.core.notification import (
    get,
    get_color,
    get_message,
    get_ci_prefix,
)


def test_get_message_deploying():
    '''
    Test get_message() constructs deploying notification message.
    '''
    result = get_message(
        DEPLOYMENT_STARTED,
        user='kabir',
        project_link='project',
        commit_link='commit',
        server_link='server'
    )
    expected_message = 'kabir is deploying project (commit) to server server.'

    assert result == expected_message


def test_get_message_deploying_with_branch():
    '''
    Test get_message() also returns deploying notification message,
    with branch link if it's provided in params.
    '''
    result = get_message(
        DEPLOYMENT_STARTED,
        user='kabir',
        project_link='project',
        commit_link='commit',
        server_link='server',
        branch_link='branch'
    )
    expected_message = 'kabir is deploying project:branch (commit) to server server.'

    assert result == expected_message


def test_get_message_deployed():
    '''
    Test get_message() constructs deployed notification message.
    '''
    result = get_message(
        DEPLOYMENT_FINISHED,
        user='kabir',
        project_link='project',
        commit_link='commit',
        server_link='server'
    )
    expected_message = 'kabir finished deploying project (commit) to server server.'

    assert result == expected_message


def test_get_message_deployed_with_branch():
    '''
    Test get_message() also returns deployed notification message,
    with branch link if it's provided in params.
    '''
    result = get_message(
        DEPLOYMENT_FINISHED,
        user='kabir',
        project_link='project',
        commit_link='commit',
        server_link='server',
        branch_link='branch'
    )
    expected_message = 'kabir finished deploying project:branch (commit) to server server.'

    assert result == expected_message


def test_get_color_on_non_ci_env():
    ''' Test get_color() on non-CI environment. '''

    env['CI'] = ''
    env['CONTINUOUS_INTEGRATION'] = ''

    result = get_color(DEPLOYMENT_STARTED, {
        'ci_deploying_color': 'blue',
        'deploying_color': 'green'
    })

    assert result == 'green'


def test_get_color_on_ci_env():
    ''' Test get_color() on CI environment. '''

    env['CI'] = 'true'

    result = get_color(DEPLOYMENT_STARTED, {
        'ci_deploying_color': 'blue',
        'deploying_color': 'green'
    })

    assert result == 'blue'


def test_get_ci_prefix_non_ci():
    ''' Test get_ci_prefix() returns empty string on non-CI env. '''
    env['CI'] = 'false'
    env['CONTINUOUS_INTEGRATION'] = 'false'

    assert get_ci_prefix() == ''


def test_get_ci_prefix_plain_text_for_unknown_ci_provider():
    '''
    Test get_ci_prefix() returns plain text CI indentifier as a prefix,
    if it's an unknown CI provider.
    '''
    env['CI'] = 'true'
    env['BOSS_RUNNING'] = 'true'
    env['TRAVIS'] = ''  # Set travis as false, as it's unknown service.

    def create_link(a, b):
        return '<{}|{}>'.format(a, b)

    result = get_ci_prefix(
        config={}, create_link=create_link
    )

    assert result == 'CI · '


def test_get_ci_prefix_retuns_link_for_travis():
    '''
    Test get_ci_prefix() returns plain text CI indentifier as a prefix,
    if it's an unknown CI provider.
    '''
    env['CI'] = 'true'
    env['BOSS_RUNNING'] = 'true'
    env['TRAVIS'] = 'true'
    env['TRAVIS_BUILD_ID'] = '59945015'
    env['TRAVIS_REPO_SLUG'] = 'test/test'

    def create_link(a, b):
        return '<{}|{}>'.format(a, b)

    result = get_ci_prefix(
        config=DEFAULT_CONFIG,
        create_link=create_link
    )
    expected = '<https://travis-ci.com/test/test/builds/59945015|CI> · '

    assert result == expected


@patch('boss.core.notification.get_color')
@patch('boss.core.notification.get_ci_prefix')
@patch('boss.core.notification.get_notification_params')
def test_get_returns_message_with_ci_prefix(gnp_m, gcp_m, gc_m):
    ''' Test get() returns message with ci prefix. '''
    gnp_m.return_value = dict(
        user='kabir',
        project_link='project',
        commit_link='commit',
        server_link='server'
    )
    gc_m.return_value = 'blue'
    gcp_m.return_value = 'CI · '

    expected = 'CI · kabir is deploying project (commit) to server server.'
    (text, _) = get(DEPLOYMENT_STARTED, notif_config={})

    assert text == expected


@patch('boss.core.notification.get_color')
@patch('boss.core.notification.get_ci_prefix')
@patch('boss.core.notification.get_notification_params')
def test_get_returns_message_without_ci_prefix(gnp_m, gcp_m, gc_m):
    ''' Test get() returns message without ci prefix. '''
    gnp_m.return_value = dict(
        user='kabir',
        project_link='project',
        commit_link='commit',
        server_link='server'
    )
    gc_m.return_value = 'blue'
    gcp_m.return_value = ''

    expected = 'kabir is deploying project (commit) to server server.'
    (text, _) = get(DEPLOYMENT_STARTED, notif_config={})

    assert text == expected
