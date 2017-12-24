''' Unit tests for boss.util module. '''

import pytest

from boss.util import (
    halt,
    info,
    echo,
    is_iterable
)


def test_halt():
    ''' Test for boss.util.halt() '''
    message = 'Test message'

    with pytest.raises(SystemExit, match=message):
        halt(message)


def test_echo(capsys):
    ''' Test for boss.util.echo() '''
    message = 'Test message'
    echo(message)

    out, _ = capsys.readouterr()

    assert message in out


def test_info(capsys):
    ''' Test for boss.util.info() '''
    message = 'Test message'
    info(message)

    out, _ = capsys.readouterr()

    assert message in out


def test_is_iterable_v0():
    ''' Test for boss.util.is_iterable() '''
    def noop():
        pass

    assert is_iterable([]) is True
    assert is_iterable({}) is True
    assert is_iterable('random string') is True

    assert is_iterable(noop) is False
    assert is_iterable(None) is False


def test_is_iterable_v1():
    '''
    Test for boss.util.is_iterable()
    Any construct that adheres to the iterator protocol should return True
    '''
    gen = (n for n in xrange(0, 10))

    assert is_iterable(gen) is True
