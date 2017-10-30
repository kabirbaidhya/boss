''' Unit tests for boss.util module. '''

import pytest

from boss.util import (
    halt,
    info,
    echo,
    merge,
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


def test_merge_v0():
    '''
    Test for boss.util.merge()
    Assert expected merge outcome when no conflicting keys are present.
    '''
    dict1 = {
        'key1': 'value1',
        'key2': {
            'key3': 'value3',
            'key4': 'value4'
        }
    }

    dict2 = {
        'keyA': 'valueA',
        'key2': {
            'keyB': 'valueB'
        }
    }

    expectedmerge = {
        'key1': 'value1',
        'key2': {
            'keyB': 'valueB',
            'key3': 'value3',
            'key4': 'value4'
        },
        'keyA': 'valueA'
    }

    merged = merge(dict1, dict2)

    assert merged == expectedmerge


def test_merge_v1():
    '''
    Test for boss.util.merge()
    Assert that second dictionary overrides conflicting keys during merge
    '''
    dict1 = {
        'key1': 'value1',
        'key2': {
            'key3': 'value3',
            'key4': 'value4'
        }
    }

    dict2 = {
        'key1': 'valueA',
        'key2': {
            'keyB': 'valueB'
        }
    }

    expectedmerge = {
        'key1': 'valueA',
        'key2': {
            'keyB': 'valueB',
            'key3': 'value3',
            'key4': 'value4'
        },
    }

    merged = merge(dict1, dict2)

    assert merged == expectedmerge


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
