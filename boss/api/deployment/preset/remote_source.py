'''
Remote Source deployment Preset.

This is a generic deployment preset, where the remote host contains the project
source code and the git repository. The deploy task would synchronize the remote
with the latest changes of the provided branch from the origin.
It then builds the project and restarts the service if needed.
'''


from fabric.api import task, hide, cd
from fabric.context_managers import shell_env

from boss.config import get_stage_config
from boss.util import remote_info, remote_print
from boss.api import git, notif, shell, runner
from boss.api.deployment.buildman import get_deploy_dir
from boss.core.util.colors import cyan
from boss.core.constants import known_scripts, notification_types


@task
def deploy(branch=None):
    ''' Deploy to remote source. '''
    stage = shell.get_stage()
    deployer_user = shell.get_user()
    branch = branch or resolve_deployment_branch(stage)
    commit = git.last_commit(remote=False, short=True)
    notif.send(notification_types.DEPLOYMENT_STARTED, {
        'user': deployer_user,
        'branch': branch,
        'commit': commit,
        'stage': stage
    })

    with cd(get_repo_path()):
        runner.run_script_safely(known_scripts.PRE_DEPLOY)

        # Get the latest code from the repository
        sync(branch)
        install_dependencies()

        # Building the app
        build(stage)
        reload_service()
        runner.run_script_safely(known_scripts.POST_DEPLOY)

    notif.send(notification_types.DEPLOYMENT_FINISHED, {
        'user': deployer_user,
        'branch': branch,
        'commit': commit,
        'stage': stage
    })

    remote_info('Deployment Completed')


def get_repo_path():
    ''' Get remote repository path. '''
    return get_deploy_dir()


def reload_service():
    ''' Reload the service after deployment. '''
    runner.run_script_safely(known_scripts.RELOAD)
    runner.run_script_safely(known_scripts.STATUS_CHECK)


def install_dependencies():
    ''' Install dependencies. '''
    runner.run_script_safely(known_scripts.PRE_INSTALL)
    runner.run_script_safely(known_scripts.INSTALL)
    runner.run_script_safely(known_scripts.POST_INSTALL)


def sync(branch=None):
    ''' Sync the changes on the branch with the remote (origin). '''
    remote_info('Fetching the latest changes.')
    git.fetch()
    branch = branch or git.current_branch()
    remote_info('Checking out to {}.'.format(cyan(branch)))
    git.checkout(branch, True)
    remote_info('Synchronizing with the latest changes.')
    git.sync(branch)


def build(stage_name=None):
    ''' Build the application. '''
    stage = shell.get_stage()

    with shell_env(STAGE=(stage_name or stage)):
        # Trigger the build script.
        runner.run_script_safely(known_scripts.PRE_BUILD)
        runner.run_script_safely(known_scripts.BUILD)
        runner.run_script_safely(known_scripts.POST_BUILD)


@task
def stop():
    ''' Stop the service. '''
    with cd(get_repo_path()):
        runner.run_script_safely(known_scripts.STOP)


@task
def restart():
    ''' Restart the service. '''
    with cd(get_repo_path()):
        runner.run_script_safely(known_scripts.RELOAD)


@task
def status():
    ''' Check the status of the service. '''
    with cd(get_repo_path()):
        runner.run_script_safely(known_scripts.STATUS_CHECK)


@task
def check():
    ''' Check the current remote branch and the last commit. '''
    with cd(get_repo_path()):
        with hide('running'):
            # Show the current branch
            remote_branch = git.current_branch()
            remote_print('Branch: {}'.format(remote_branch))
            # Show the last commit
            git.show_last_commit()


def resolve_deployment_branch(stage):
    ''' Resolve the branch or ref for deployment. '''
    stage_config = get_stage_config(stage)

    if stage_config['deployment']['use_local_ref']:
        return git.get_local_ref()

    # Resolve the default branch for the provided
    # `stage` from the config.
    return stage_config['branch']
