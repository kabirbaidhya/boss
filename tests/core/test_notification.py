''' Test boss.core.notification. '''
from boss.core.constants.notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED
)
from boss.core.notification import (
    get_message
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
