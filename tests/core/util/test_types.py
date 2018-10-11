''' Unit tests for boss.core.util.types module. '''

from boss.core.util.types import (
    is_iterable,
    is_string,
    is_dict
)


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


def test_is_string():
    ''' Test is_string() function. '''
    assert is_string('') is True
    assert is_string('Test') is True
    assert is_string("Hello") is True
    assert is_string(u"Hello") is True
    assert is_string(True) is False
    assert is_string(None) is False


def test_is_dict():
    ''' Test is_dict() function. '''
    assert is_dict('') is False
    assert is_dict('Test') is False
    assert is_dict(u"Hello") is False
    assert is_dict(None) is False
    assert is_dict([]) is False
    assert is_dict({}) is True
    assert is_dict({'foo': 'bar'}) is True
    assert is_dict(dict()) is True
