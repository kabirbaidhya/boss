
from mock import patch
from unittest import TestCase

from boss.core import initializer


class TestInitializer(TestCase):
    ''' Tests for boss.core.initializer module. '''

    @patch('boss.core.fs.exists')
    def test_initialize_if_all_files_already_exist(self, mock_exists):
        ''' Test initializer.initialize() works if all the files exist already. '''
        mock_exists.return_value = True
        files_written = initializer.initialize()

        assert not files_written

    @patch('boss.core.fs.write')
    @patch('boss.core.fs.exists')
    def test_initialize_if_no_files_exist(self, mock_exists, mock_write):
        ''' Test initializer.initilize() works if none of the files exist. '''
        mock_exists.return_value = False
        files_written = initializer.initialize()

        assert len(files_written) == mock_write.call_count
