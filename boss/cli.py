from . import __version__
import click


@click.version_option(__version__, message='%(version)s')
@click.command()
def main():
    click.echo('Boss says!')
