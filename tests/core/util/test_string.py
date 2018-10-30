''' Unit tests for boss.core.util.string module. '''


from boss.core.util.string import strip_ansi, is_quoted
from boss.core.util.colors import red


def test_strip_ansi():
    '''
    Test strip_ansi() removes console color codes from a string.
    '''
    text = 'This is just a ' + red('test.')
    plain_text = 'This is just a test.'

    assert plain_text == strip_ansi(text)


def test_strip_ansi_returns_same_string_for_plain_text():
    '''
    Test strip_ansi() returns the same string if it's plain text.
    '''
    text = 'This is just a test.'
    plain_text = 'This is just a test.'

    assert plain_text == strip_ansi(text)


def test_strip_ansi_with_empty_string_and_none():
    '''
    Test strip_ansi() with empty string and None as inputs.
    '''
    assert strip_ansi('') == ''
    assert strip_ansi(None) is None


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
