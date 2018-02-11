'''
Remote Source deployment Preset.

This is a generic deployment preset, where the remote host contains the project
source code and the git repository. The deploy task would synchronize the remote
with the latest changes of the provided branch from the origin.
It then builds the project and restarts the service if needed.
'''


from fabric.api import task, hide, cd
from fabric.context_managers import shell_env

from boss import BASE_PATH, __version__
from boss.config import get_stage_config, get as get_config
from boss.util import remote_info, remote_print
from boss.api import git, notif, shell, runner, fs
from boss.core.util.colors import cyan
from boss.core.constants import known_scripts, notification_types
from boss.api.deployment.buildman import get_deploy_dir

REMOTE_SCRIPT = '/sync-{}.sh'.format(__version__)
REPOSITORY_PATH = '/repo'


@task
def deploy(branch=None):
    ''' Deploy to remote source. '''
    stage = shell.get_stage()
    branch = branch or get_stage_config(stage)['branch']
    params = dict(
        user=shell.get_user(),
        stage=stage,
        branch=branch
    )
    script_path = get_deploy_dir() + REMOTE_SCRIPT
    repo_path = get_deploy_dir() + REPOSITORY_PATH

    # Check if the script exists (with version) on the remote.
    if not fs.exists(script_path):
        runner.run('mkdir -p ' + repo_path)
        fs.upload(BASE_PATH + '/misc/scripts/sync.sh', script_path)

    notif.send(notification_types.DEPLOYMENT_STARTED, params)

    env_vars = dict(
        STAGE=stage,
        BRANCH=branch,
        REPOSITORY_PATH=repo_path,
        REPOSITORY_URL=get_config()['repository_url']
    )

    with hide('running'):
        with shell_env(**env_vars):
            # Run the sync script on the remote
            runner.run('sh ' + script_path)

    with cd(repo_path):
        install_dependencies()

        # Building the app
        build(stage)
        reload_service()

    notif.send(notification_types.DEPLOYMENT_FINISHED, params)
    remote_info('Deployment Completed')


def reload_service():
    ''' Reload the service after deployment. '''
    runner.run_script_safely(known_scripts.RELOAD)
    runner.run_script_safely(known_scripts.STATUS_CHECK)


def install_dependencies():
    ''' Install dependencies. '''
    runner.run_script_safely(known_scripts.INSTALL)


@task
def sync(branch=None):
    ''' Sync the changes on the branch with the remote (origin). '''
    remote_info('Fetching the latest changes.')
    git.fetch()
    branch = branch or git.current_branch()
    remote_info('Checking out to branch {}.'.format(cyan(branch)))
    git.checkout(branch, True)
    remote_info('Synchronizing with the latest changes.')
    git.sync(branch)


@task
def build(stage_name=None):
    ''' Build the application. '''
    stage = shell.get_stage()

    with shell_env(STAGE=(stage_name or stage)):
        # Trigger the build script.
        runner.run_script_safely(known_scripts.BUILD)


@task
def stop():
    ''' Stop the service. '''
    runner.run_script_safely(known_scripts.STOP)


@task
def restart():
    ''' Restart the service. '''
    runner.run_script_safely(known_scripts.RELOAD)


@task
def status():
    ''' Check the status of the service. '''
    runner.run_script_safely(known_scripts.STATUS_CHECK)


@task
def check():
    ''' Check the current remote branch and the last commit. '''
    with hide('running'):
        # Show the current branch
        remote_branch = git.current_branch()
        remote_print('Branch: {}'.format(remote_branch))
        # Show the last commit
        git.show_last_commit()
