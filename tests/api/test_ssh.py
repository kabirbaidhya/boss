''' Tests for ssh module. '''

from mock import patch, Mock
from boss.api.ssh import put
from paramiko import SFTP


# @patch('boss.state.get')
# def test_put(get_m):
#     ''' Test put() works. '''

#     attrs = {'open_sftp.return_value': Mock(SFTP)}
#     connection_m = Mock(**attrs)

#     def get_side_effect(key):
#         values = {
#             'env': {
#                 'host_string': 'test-host'
#             },
#             'connections': {
#                 'test-host': connection_m
#             }
#         }

#         return values[key]

#     get_m.side_effect = get_side_effect

#     put('localfile', 'remotefile')
