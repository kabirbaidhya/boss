from . import __version__
import click

from .core import initializer

INTERACTIVE_INIT_HELP = 'Start an interactive session to compose config file'


@click.version_option(__version__, message='%(version)s')
@click.group()
def main():
    ''' Boss CLI. '''
    pass


@main.command('init')
@click.option('--interactive', '-i', is_flag=True, help=INTERACTIVE_INIT_HELP)
def init(interactive):
    ''' Initialize a project directory for boss. '''
    initializer.setup_boss_home()
    files_written = initializer.initialize(interactive)

    if not files_written:
        click.echo('Already initialized.')
        return

    # Print the files generated while initializing.
    for f in files_written:
        click.echo('Generated file: {}'.format(f))
