from fabric.api import run
from boss import config


def get_configured_service():
    return config['service']


def enable(service=None):
    run('sudo systemctl enable %s' % service or get_configured_service())


def restart(service=None):
    run('sudo systemctl restart %s' % service or get_configured_service())


def status(service=None):
    run('sudo systemctl status %s' % service or get_configured_service())


def stop(service=None):
    run('sudo systemctl stop %s' % service or get_configured_service())
