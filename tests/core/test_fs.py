
from unittest import TestCase
from mock import patch, mock_open

from boss.core import fs


class TestFs(TestCase):
    ''' Tests for boss.core.fs module. '''

    @patch('os.path.exists')
    def test_exists(self, result):
        ''' Test fs.exists() works. '''
        filename = 'somefile'
        fs.exists(filename)
        result.assert_called_with(filename)

    def test_read(self):
        ''' Test fs.read() works. '''
        filename = 'somefile'
        data = 'somedata'

        with patch('__builtin__.open', mock_open(read_data=data)) as mock_file:
            assert fs.read(filename) == data
            mock_file.assert_called_with(filename, 'r')

    def test_write(self):
        ''' Test fs.write() works. '''
        filename = 'somefile'
        data = 'somedata'
        m = mock_open()

        with patch('__builtin__.open', m) as mock_file:
            fs.write(filename, data)
            mock_file.assert_called_with(filename, 'w')
            m().write.assert_called_with(data)
