'''
Default tasks Module.
'''

from fabric.api import run, hide, task
from fabric.context_managers import shell_env
from .util import info, warn_deprecated
from .api import git, notif, shell, npm, systemctl
from .config import fallback_branch, get_service, get_stage_config, get as get_config

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
    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': shell.get_user(),
        'branch': branch,
        'stage': stage
    })

    # Get the latest code from the repository
    sync(branch)

    # Installing dependencies
    npm.install()

    # Building the app
    build(stage)

    service = get_service()

    if service:
        # Enable and Restart the service if service is provided
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
    git.checkout(branch, True)
    info('Syncing the latest changes of the %s branch' % branch)
    git.sync(branch)


@task
def build(stage_name=None):
    ''' Build the application. '''
    with shell_env(STAGE=(stage_name or stage)):
        npm.run('build')


@task
def stop():
    ''' Stop the systemctl service. '''
    # Deprecate everything that is tightly coupled to systemd
    # as they are subject to change in the major future release.
    warn_deprecated(
        'The `stop` task is deprecated and will be either removed' +
        ' or subject to change in the major future release.'
    )
    systemctl.stop(get_service())


@task
def restart():
    ''' Restart the service. '''
    # Deprecate everything that is tightly coupled to systemd
    # as they are subject to change in the major future release.
    warn_deprecated(
        'The `restart` task is deprecated and will be either removed' +
        ' or subject to change in the major future release.'
    )
    systemctl.restart(get_service())


@task
def status():
    ''' Get the status of the service. '''
    warn_deprecated(
        'The `status` task is deprecated and will be either removed' +
        ' or subject to change in the major future release.'
    )
    systemctl.status(get_service())


@task
def logs():
    ''' Tail the logs. '''
    # Tail the logs from journalctl if
    # systemctl service is configured
    if get_service():
        warn_deprecated(
            'Using journalctl to tail the logs from ' +
            'configured service is deprecated. ' +
            'You\'ll need to provide the config explicitly for logging.'
        )
        run('sudo journalctl -f -u %s' % get_service())
        return

    # Get the logging config
    stage_specific_logging = get_stage_config(stage).get('logging')
    logging_config = stage_specific_logging or get_config().get('logging')

    if logging_config and logging_config.get('files'):
        # Tail the logs from log files
        log_paths = ' '.join(logging_config.get('files'))
        run('tail -f ' + log_paths)


__all__ = ['deploy', 'check', 'sync', 'build',
           'stop', 'restart', 'status', 'logs']
