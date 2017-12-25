''' Tests for ssh module. '''

from mock import patch, Mock

from boss.api.ssh import resolve_sftp_client


@patch('boss.api.ssh.state.get')
def test_resolve_sftp_client_existing_client(get_m):
    '''
    Test resolve_sftp_client() returns an
    existing sftp connection if it exists.
    '''

    sftp_client = Mock(foo='bar')

    def side_effect(x):
        d = {
            'env': Mock(host_string='localhost'),
            'sftp_connections': {
                'localhost': sftp_client
            }
        }

        return d[x]

    get_m.side_effect = side_effect
    result = resolve_sftp_client()

    assert result == sftp_client


@patch('boss.api.ssh.state.get')
def test_resolve_sftp_client_new_client(get_m):
    '''
    Test resolve_sftp_client() returns
    a new sftp connection if it doesn't exists.
    '''

    sftp_client = Mock(foo='bar')
    attrs = {'open_sftp.return_value': sftp_client}
    client = Mock(**attrs)

    def side_effect(x):
        d = {
            'env': Mock(host_string='localhost'),
            'sftp_connections': {},
            'connections': {
                'localhost': client
            }
        }

        return d[x]

    get_m.side_effect = side_effect
    result = resolve_sftp_client()

    assert result == sftp_client
