''' Unit tests for boss.config module. '''

from mock import patch
from boss.state import get


def test_get():
    ''' Test get() returns a copy of boss current state. '''
    state_m = {'foo': 'bar'}

    with patch.dict('boss.state._state', state_m):
        result = get()

        assert result['foo'] == state_m['foo']
