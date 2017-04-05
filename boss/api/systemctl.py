'''
Module for systemctl API.
'''

from fabric.api import run


def enable(service):
    ''' Enable the service. '''
    run('sudo systemctl enable %s' % service)


def start(service):
    ''' Start the service. '''
    run('sudo systemctl start %s' % service)


def restart(service):
    ''' Restart the service. '''
    run('sudo systemctl restart %s' % service)


def status(service):
    ''' Check the status of the service. '''
    run('sudo systemctl status %s' % service)


def stop(service):
    ''' Stop the service. '''
    run('sudo systemctl stop %s' % service)
