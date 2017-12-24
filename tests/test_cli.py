''' Tests for CLI. '''

import os
from click.testing import CliRunner

from boss import __version__
from boss.cli import main as cli
from boss.constants import (
    FABFILE_PATH,
    BOSS_HOME_PATH,
    BOSS_CACHE_PATH,
    DEFAULT_CONFIG_FILE
)


def test_version_option():
    ''' Test version option. '''
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])

    assert result.exit_code == 0
    assert result.output.strip() == __version__


def test_init_command():
    '''
    Test init command generates config files and
    doees setup boss home directory.
    '''
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['init'])

        assert result.exit_code == 0
        assert os.path.exists(BOSS_HOME_PATH)
        assert os.path.exists(BOSS_CACHE_PATH)
        assert os.path.exists(FABFILE_PATH)
        assert os.path.exists(DEFAULT_CONFIG_FILE)
