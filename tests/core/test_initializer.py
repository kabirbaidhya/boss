''' Tests for boss.core.initializer module. '''

from mock import patch, call

from boss.constants import BOSS_HOME_PATH, BOSS_CACHE_PATH
from boss.core import initializer


@patch('boss.core.fs.exists')
def test_initialize_if_all_files_already_exist(mock_exists):
    ''' Test initializer.initialize() works if all the files exist already. '''
    interactive_flag = False
    mock_exists.return_value = True
    files_written = initializer.initialize(interactive_flag)

    assert not files_written


@patch('boss.core.fs.write')
@patch('boss.core.fs.exists')
def test_initialize_if_no_files_exist(mock_exists, mock_write):
    ''' Test initializer.initilize() works if none of the files exist. '''
    interactive_flag = False
    mock_exists.return_value = False
    files_written = initializer.initialize(interactive_flag)

    assert len(files_written) == mock_write.call_count


@patch('boss.core.fs.exists')
@patch('boss.core.initializer.mkdir')
def test_setup_boss_home(mock_mkdir, mock_exists):
    '''
    Test directories are created if
    boss home path doesn't exist.
    '''
    mock_exists.return_value = False
    initializer.setup_boss_home()
    mock_mkdir.assert_has_calls([
        call(BOSS_HOME_PATH),
        call(BOSS_CACHE_PATH)
    ])
