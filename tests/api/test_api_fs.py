''' Tests for boss.api.fs module. '''

from mock import patch
from boss.api.fs import rm_rf


@patch('boss.api.ssh.run')
def test_rm_rf(r_m):
    ''' Test rm_rf() works for a single file. '''

    rm_rf('hello.txt')

    r_m.assert_called_with('rm -rf hello.txt')


@patch('boss.api.ssh.run')
def test_rm_rf_with_multiple_files(r_m):
    ''' Test rm_rf() works for multiple files. '''

    rm_rf(['hello.txt', 'abc.txt', 'xyz.txt'])

    r_m.assert_called_with('rm -rf hello.txt abc.txt xyz.txt')
