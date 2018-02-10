''' Tests for boss.api.git module. '''

from boss.api.git import get_commit_url, get_tree_url


def test_get_commit_url():
    ''' Test get_commit_url(). '''
    url = get_commit_url('f626609', 'https://github.com/kabirbaidhya/boss')

    assert url == 'https://github.com/kabirbaidhya/boss/commit/f626609'


def test_get_tree_url():
    ''' Test get_tree_url(). '''
    url = get_tree_url('master', 'https://github.com/kabirbaidhya/boss')

    assert url == 'https://github.com/kabirbaidhya/boss/tree/master'
