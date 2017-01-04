"""
boss

Usage:
  boss hello
  boss -h | --help
  boss --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  boss hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rdegges/boss-cli
"""

import sys
from inspect import getmembers, isclass
from docopt import docopt

import boss
from . import __version__ as VERSION
from .api import config

module = sys.modules[__name__]
boss.config.update(config.get_default())


def main():
    """Main CLI entrypoint."""
    from boss import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            boss.config.update(config.load())
            cmd_module = getattr(commands, k)
            commands = getmembers(cmd_module, isclass)
            command = [command[1]
                       for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
