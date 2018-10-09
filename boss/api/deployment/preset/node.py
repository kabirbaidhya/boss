# -*- coding: utf-8 -*-
'''
Node Application Deployment preset.

This would be useful for deploying node js projects to the remote server.
Here the source is built locally and uploaded to the server, then the application service
is started on restarted on the remote server.
'''

from datetime import datetime
from fabric.api import task, cd

from boss.util import remote_info
from boss.api import shell, notif, runner, fs, git
from boss.config import get as get_config
from boss.core.output import halt, info
from boss.core.constants import known_scripts, notification_types
from .. import buildman


@task
def builds():
    ''' Display the build history. '''
    # Load the build history
    history = buildman.load_history()
    buildman.display_list(history)


@task
def rollback(id=None):
    ''' Zero-Downtime deployment rollback for the frontend. '''
    buildman.rollback(id)

    # Reload the service after build has been rollbacked.
    reload_service()


@task(alias='info')
def buildinfo(id=None):
    ''' Print the build information. '''
    buildman.display(id)


@task
def setup():
    ''' Setup remote host for deployment. '''
    buildman.setup_remote(quiet=False)


def upload_included_files(files, remote_path):
    ''' Upload the local files if they were to be included. '''
    for filename in files:
        # Skip upload if the file doesn't exist.
        if not fs.exists(filename, remote=False):
            continue

        fs.upload(filename, remote_path)


@task
def deploy():
    ''' Zero-Downtime deployment for the backend. '''
    config = get_config()
    stage = shell.get_stage()
    is_first_deployment = not buildman.is_remote_setup()

    branch = git.current_branch(remote=False)
    commit = git.last_commit(remote=False, short=True)
    info('Deploying <{branch}:{commit}> to the {stage} server'.format(
        branch=branch,
        commit=commit,
        stage=stage
    ))

    tmp_path = fs.get_temp_filename()
    build_dir = buildman.resolve_local_build_dir()
    included_files = config['deployment']['include_files']

    deployer_user = shell.get_user()

    notif.send(notification_types.DEPLOYMENT_STARTED, {
        'user': deployer_user,
        'commit': commit,
        'branch': branch,
        'stage': stage
    })
    runner.run_script_safely(known_scripts.PRE_DEPLOY)

    (release_dir, current_path) = buildman.setup_remote()

    timestamp = datetime.utcnow()
    build_id = timestamp.strftime('%Y%m%d%H%M%S')
    build_name = buildman.get_build_name(build_id)
    build_compressed = build_name + '.tar.gz'
    release_path = release_dir + '/' + build_name
    dist_path = build_name + '/dist'

    buildman.build(stage, config)

    info('Compressing the build')
    fs.tar_archive(build_compressed, build_dir, remote=False)

    info('Uploading the build {} to {}'.format(build_compressed, tmp_path))
    fs.upload(build_compressed, tmp_path)

    # Remove the compressed build from the local directory.
    fs.rm(build_compressed, remote=False)

    # Once, the build is uploaded to the remote,
    # set things up in the remote server.
    with cd(release_dir):
        remote_info('Extracting the build {}'.format(build_compressed))
        # Create a new directory for the build in the remote.
        fs.mkdir(dist_path, nested=True)

        # Extract the build.
        fs.tar_extract(tmp_path, dist_path)

        # Remove the uploaded archived from the temp path.
        fs.rm_rf(tmp_path)

        # Upload the files to be included eg: package.json file
        # to the remote build location.
        upload_included_files(included_files, release_path)

        remote_info('Pointing the current symlink to the latest build')
        fs.update_symlink(release_path, current_path)

    # Change directory to the release path.
    with cd(current_path):
        install_remote_dependencies()

    # Start or restart the application service.
    start_or_reload_service(is_first_deployment)

    # Save build history
    buildman.record_history({
        'id': build_id,
        'path': release_path,
        'branch': branch,
        'commit': commit,
        'stage': stage,
        'createdBy': deployer_user,
        'timestamp': timestamp.strftime(buildman.TS_FORMAT)
    })

    runner.run_script_safely(known_scripts.POST_DEPLOY)

    # Send deployment finished notification.
    notif.send(notification_types.DEPLOYMENT_FINISHED, {
        'user': deployer_user,
        'branch': branch,
        'commit': commit,
        'stage': stage
    })

    remote_info('Deployment Completed')


def install_remote_dependencies():
    ''' Install dependencies on the remote host. '''
    remote_info('Installing dependencies on the remote')
    runner.run_script_safely(known_scripts.PRE_INSTALL)

    if runner.is_script_defined(known_scripts.INSTALL_REMOTE):
        runner.run_script_safely(known_scripts.PRE_INSTALL_REMOTE)
        runner.run_script(known_scripts.INSTALL_REMOTE)
        runner.run_script_safely(known_scripts.POST_INSTALL_REMOTE)
    else:
        runner.run_script_safely(known_scripts.INSTALL)

    runner.run_script_safely(known_scripts.POST_INSTALL)


def start_or_reload_service(has_started=False):
    ''' Start or reload the application service. '''
    with cd(buildman.get_deploy_dir()):
        if runner.is_script_defined(known_scripts.START_OR_RELOAD):
            remote_info('Starting/Reloading the service.')
            runner.run_script(known_scripts.START_OR_RELOAD)

        elif has_started and runner.is_script_defined(known_scripts.RELOAD):
            remote_info('Reloading the service.')
            runner.run_script_safely(known_scripts.RELOAD)

        elif runner.is_script_defined(known_scripts.START):
            remote_info('Starting the service.')
            runner.run_script(known_scripts.START)


def reload_service():
    ''' Restart the application service. '''
    with cd(buildman.get_deploy_dir()):
        remote_info('Reloading the service.')
        runner.run_script_safely(known_scripts.RELOAD)


def stop_service():
    ''' Stop the application service. '''
    with cd(buildman.get_deploy_dir()):
        remote_info('Stopping the service.')
        runner.run_script_safely(known_scripts.STOP)


@task(alias='reload')
def restart():
    ''' Restart the service. '''
    start_or_reload_service(True)


@task
def stop():
    ''' Stop the service. '''
    stop_service()


@task
def status():
    ''' Get the status of the service. '''
    with cd(buildman.get_current_path()):
        runner.run_script(known_scripts.STATUS_CHECK)


@task
def run(script):
    ''' Run a custom script. '''
    # Run a custom script defined in the config.
    # Change the current working directory to the node application
    # before running the script.

    with cd(buildman.get_current_path()):
        try:
            runner.run_script(script)
        except RuntimeError as e:
            halt(str(e))


@task(alias='list')
def services():
    ''' List the services running for the application. '''
    with cd(buildman.get_current_path()):
        runner.run_script(known_scripts.LIST_SERVICES)
