'''
Default tasks Module.
'''

from fabric.api import run, hide, task
from fabric.context_managers import shell_env
from .api import git, notif, shell, npm, systemctl
from .util import info
from .config import fallback_branch, get_service

stage = shell.get_stage()


@task
def check():
    ''' Check the current remote branch and the last commit. '''
    with hide('running'):
        # Show the current branch
        remote_branch = git.remote_branch()
        run('echo "Branch: %s"' % remote_branch)
        # Show the last commit
        git.show_last_commit()


@task
def deploy(branch=None):
    ''' The deploy task. '''
    branch = branch or fallback_branch(stage)
    service = get_service()
    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': shell.get_user(),
        'branch': branch,
        'stage': stage
    })

    # Get the latest code from the repository
    sync(branch)

    systemctl.stop(service)
    # Installing dependencies
    npm.install()

    # Building the app
    build(stage)

    # Enable and Restart the service
    systemctl.enable(service)
    systemctl.restart(service)
    systemctl.status(service)

    notif.send(notif.DEPLOYMENT_FINISHED, {
        'branch': branch,
        'stage': stage
    })

    info('Deployment Completed')


@task
def sync(branch=None):
    ''' Sync the changes on the branch with the remote (origin). '''
    git.fetch()
    branch = branch or git.remote_branch()
    info('Checking out to %s branch' % branch)
    git.checkout(branch)
    info('Syncing the latest changes of the %s branch' % branch)
    git.sync(branch)


@task
def build(stage_name=None):
    ''' Build the application. '''
    with shell_env(STAGE=(stage_name or stage)):
        npm.run('build')


@task
def stop():
    ''' Stop the service. '''
    systemctl.stop(get_service())


@task
def restart():
    ''' Restart the service. '''
    systemctl.restart(get_service())


@task
def status():
    ''' Get the status of the service. '''
    systemctl.status(get_service())


@task
def logs():
    ''' Tail the logs. '''
    run('sudo journalctl -f -u %s' % get_service())

__all__ = ['deploy', 'check', 'sync', 'build',
           'stop', 'restart', 'status', 'logs']
