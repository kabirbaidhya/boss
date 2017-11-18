''' Unit tests for boss.core.util.string module. '''


from boss.core.util.string import strip_ansi
from fabric.colors import red


def test_strip_ansi():
    text = 'This is just a ' + red('test.')
    plain_text = 'This is just a test.'

    assert plain_text == strip_ansi(text)
