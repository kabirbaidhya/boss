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

REMOTE_SCRIPT = '/deploy-{}.sh'.format(__version__)
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
    notif.send(notification_types.DEPLOYMENT_STARTED, params)
    run_deploy_script(stage, branch)
    notif.send(notification_types.DEPLOYMENT_FINISHED, params)
    remote_info('Deployment Completed')


def get_repo_path():
    ''' Get remote repository path. '''
    return get_deploy_dir() + REPOSITORY_PATH


def run_deploy_script(stage, branch):
    ''' Run the deployment script on the remote host. '''
    script_path = get_deploy_dir() + REMOTE_SCRIPT
    repo_path = get_repo_path()

    # Check if the script exists (with version) on the remote.
    if not fs.exists(script_path):
        with hide('running'):
            runner.run('mkdir -p ' + repo_path)
            fs.upload(
                BASE_PATH + '/misc/scripts/remote-source-deploy.sh',
                script_path
            )

    env_vars = dict(
        STAGE=stage,
        BRANCH=branch,
        REPOSITORY_PATH=repo_path,
        REPOSITORY_URL=get_config()['repository_url'],
        SCRIPT_BUILD=runner.get_script_cmd(known_scripts.BUILD),
        SCRIPT_RELOAD=runner.get_script_cmd(known_scripts.RELOAD),
        SCRIPT_INSTALL=runner.get_script_cmd(known_scripts.INSTALL),
        SCRIPT_STATUS_CHECK=runner.get_script_cmd(known_scripts.STATUS_CHECK)
    )

    with hide('running'):
        with shell_env(**env_vars):
            # Run the sync script on the remote
            runner.run('sh ' + script_path)


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
    with cd(get_repo_path()):
        with hide('running'):
            # Show the current branch
            remote_branch = git.current_branch()
            remote_print('Branch: {}'.format(remote_branch))
            # Show the last commit
            git.show_last_commit()
