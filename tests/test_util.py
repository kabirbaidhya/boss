''' Unit tests for boss.util module. '''

import pytest

from boss.util import (
    halt,
    info,
    echo
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
