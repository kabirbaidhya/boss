''' Unit tests for boss.core.util.string module. '''


from boss.core.util.string import strip_ansi, is_quoted
from boss.core.util.colors import red


def test_strip_ansi():
    text = 'This is just a ' + red('test.')
    plain_text = 'This is just a test.'

    assert plain_text == strip_ansi(text)


def test_is_quoted():
    '''
    Test is_quoted returns True only
    for the quoted string values.
    '''
    assert is_quoted('"Hello World"') is True
    assert is_quoted('\'Hello World\'') is True
    assert is_quoted('Hello World') is False
    assert is_quoted('\'Hello World') is False
    assert is_quoted('"Hello World') is False
    assert is_quoted('Hello World"') is False
    assert is_quoted('Hello World\'') is False
