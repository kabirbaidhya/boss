from . import __version__
import click

from .core import initializer


@click.version_option(__version__, message='%(version)s')
@click.group()
def main():
    ''' Boss CLI. '''
    pass


@main.command('init')
def init():
    ''' Initialize a project directory for boss. '''
    files_written = initializer.initialize()

    if not files_written:
        click.echo('Already initialized.')
        return

    # Print the files generated while initializing.
    for f in files_written:
        click.echo('Generated file: {}'.format(f))
