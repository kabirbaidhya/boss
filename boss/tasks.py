'''
Default tasks Module.
'''

from fabric.api import run, hide, task
from .api import git, notif, shell, npm, systemctl
from .util import info
from .config import get as get_config, fallback_branch

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
    config = get_config()
    branch = branch or fallback_branch(stage)
    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': shell.get_user(),
        'branch': branch,
        'stage': stage
    })

    # Get the latest code from the repository
    sync(branch)

    systemctl.stop(config['service'])
    # Installing dependencies
    npm.install()

    # Building the app
    build(stage)

    # Enable and Restart the service
    systemctl.enable(config['service'])
    systemctl.restart(config['service'])
    systemctl.status(config['service'])

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
def build(stage=None):
    ''' Build the application. '''
    npm.run('build')


__all__ = ['deploy', 'check', 'sync', 'build']
