''' Tests for CLI. '''

import os
import envoy

from click.testing import CliRunner
from boss import __version__ as VERSION
from boss.constants import DEFAULT_CONFIG_FILE, FABFILE_PATH
from boss.cli import main as cli


def test_version_option():
    ''' Test version option. '''
    output = envoy.run('boss --version').std_out
    assert output.strip() == VERSION


def test_init_command():
    ''' Test init command generates files. '''
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['init'])

        assert result.exit_code == 0
        assert os.path.exists(FABFILE_PATH)
        assert os.path.exists(DEFAULT_CONFIG_FILE)
