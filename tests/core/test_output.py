''' Tests for boss.core.output module. '''

import pytest

from boss.core.output import halt, info, echo


def test_halt():
    ''' Test for halt() '''
    message = 'Test message'

    with pytest.raises(SystemExit, match=message):
        halt(message)


def test_echo(capsys):
    ''' Test for echo() '''
    message = 'Test message'
    echo(message)

    out, _ = capsys.readouterr()

    assert message in out


def test_info(capsys):
    ''' Test for info() '''
    message = 'Test message'
    info(message)

    out, _ = capsys.readouterr()

    assert message in out
