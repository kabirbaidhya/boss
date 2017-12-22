# ''' Unit tests for boss.config module. '''

# from mock import patch
# from boss.state import get


# def test_get():
#     ''' Test get() returns a copy of boss current state. '''

#     with patch.dict('boss.state._state', {'foo': 'bar'}):
#         result = get()

#         assert result['foo'] == 'bar'


# def test_get_returns_fabric_state_too():
#     ''' Test get() returns state along with fabric's state. '''

#     with patch.dict('boss.state._state', {'foo': 'bar'}):
#         with patch.dict('fabric.state.env', {'a': 'test'}):
#             with patch.dict('fabric.state.connections', {'b': 'bar'}):
#                 result = get()

#                 assert result['foo'] == 'bar'
#                 assert result['env']['a'] == 'test'
#                 assert result['connections']['b'] == 'bar'


# def test_get_by_key():
#     ''' Test get(key) returns a value if found. '''

#     with patch.dict('boss.state._state', {'foo': 'something'}):
#         result = get('foo')

#         assert result == 'something'
