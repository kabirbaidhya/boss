''' Tests for boss.core.env module '''

from boss.core import env

ENV_DEF_SIMPLE = '''
NODE_ENV=development
APP_PORT=3000
APP_BASE_URL=http://localhost:3000
'''

ENV_DEF_WITH_INDENTATION = '''
    VAR1=development
    VAR2=3000
'''

ENV_DEF_WITH_COMMENTS = '''
NODE_ENV=development
# APP_PORT=3000
#APP_BASE_URL=http://localhost:3000
# This is just a test

ANOTHER_VAR=Foo Bar
'''

ENV_DEF_WITH_QUOTED_VALUES = '''
VAR1="Foo"
VAR2='Bar'
'''


def test_parse_simple_env_def():
    ''' Test it parses a simple env declaration. '''
    result = env.parse(ENV_DEF_SIMPLE)

    assert result['NODE_ENV'] == 'development'
    assert result['APP_PORT'] == '3000'
    assert result['APP_BASE_URL'] == 'http://localhost:3000'


def test_parse_env_def_with_indentation():
    ''' Test it parses a simple env declaration. '''
    result = env.parse(ENV_DEF_WITH_INDENTATION)

    assert result['VAR1'] == 'development'
    assert result['VAR2'] == '3000'


def test_parse_env_def_with_quoted_values():
    ''' Test it parses a simple env declaration. '''
    result = env.parse(ENV_DEF_WITH_QUOTED_VALUES)

    assert result['VAR1'] == 'Foo'
    assert result['VAR2'] == 'Bar'
