''' Tests for boss.api.git module. '''

from mock import patch
from boss.api.git import (
    get_commit_url,
    get_tree_url,
    get_local_ref
)


def test_get_commit_url():
    ''' Test get_commit_url(). '''
    url = get_commit_url('f626609', 'https://github.com/kabirbaidhya/boss')

    assert url == 'https://github.com/kabirbaidhya/boss/commit/f626609'


def test_get_tree_url():
    ''' Test get_tree_url(). '''
    url = get_tree_url('master', 'https://github.com/kabirbaidhya/boss')

    assert url == 'https://github.com/kabirbaidhya/boss/tree/master'


def test_get_commit_url_when_no_repository_url():
    ''' Test get_commit_url() returns the commit, if repository_url is not provided. '''
    url = get_commit_url('f626609')

    assert url is None


def test_get_tree_url_when_no_repository_url():
    ''' Test get_tree_url() returns the ref, if repository_url is not provided. '''
    url = get_tree_url('master')

    assert url is None


@patch('boss.api.git.current_branch', return_value='my-branch')
def test_get_local_ref_returns_branch(_):
    ''' Test get_local_ref() returns the local branch. '''
    assert get_local_ref() == 'my-branch'


@patch('boss.api.git.current_branch', return_value='HEAD')
@patch('boss.api.git.last_commit', return_value='a12345bc')
def test_get_local_ref_returns_commit_hash(_, __):
    '''
    Test get_local_ref() returns the commit hash,
    if local branch is not available.
    '''
    assert get_local_ref() == 'a12345bc'
