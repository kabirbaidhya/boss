# -*- coding: utf-8 -*-
'''
Node Application Deployment preset.

This would be useful for deploying node js projects to the remote server.
Here the source is built locally and uploaded to the server, then the application service
is started on restarted on the remote server.
'''
import os
from datetime import datetime
from fabric.api import task, cd

from boss.util import remote_info
from boss.config import get as get_config, get_stage_config
from boss.core.output import halt, info, echo
from boss.core.fs import exists as exists_local
from boss.core.constants import known_scripts, notification_types
from boss.api import shell, notif, runner, fs, git
from boss.api.transfers import BulkUploader
from boss.api.deployment import buildman


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


@task
def deploy():
    ''' Zero-Downtime deployment for the backend. '''
    config = get_config()
    stage = shell.get_stage()
    is_remote_setup = buildman.is_remote_setup()
    is_first_deployment = not is_remote_setup

    if is_remote_setup and buildman.is_remote_up_to_date():
        echo('Remote build is already up to date.')
        return

    branch = git.current_branch(remote=False)
    commit = git.last_commit(remote=False, short=True)
    info('Deploying <{branch}:{commit}> to the {stage} server'.format(
        branch=branch,
        commit=commit,
        stage=stage
    ))

    build_dir = os.path.abspath(buildman.resolve_local_build_dir())
    included_files = config['deployment']['include_files']
    deployer_user = shell.get_user()
    notif_params = dict(
        user=deployer_user,
        commit=commit,
        branch=branch,
        stage=stage
    )
    notif.send(notification_types.DEPLOYMENT_STARTED, notif_params)
    runner.run_script_safely(known_scripts.PRE_DEPLOY)

    (release_dir, current_path) = buildman.setup_remote()

    timestamp = datetime.utcnow()
    build_id = timestamp.strftime('%Y%m%d%H%M%S')
    build_name = buildman.get_build_name(build_id)
    release_path = os.path.join(release_dir + '/' + build_name)
    dist_path = os.path.join(release_dir, build_name + '/dist')

    buildman.build(stage, config)

    uploader = BulkUploader()
    uploader.add(build_dir, dist_path)

    # Upload the files to be included eg: package.json file
    # to the remote build location.
    for filename in included_files:
        path = os.path.abspath(filename)
        # Add for upload if the file exist.
        if exists_local(path):
            uploader.add(path, release_path)

    uploader.upload()
    remote_info('Updating the current symlink')
    fs.update_symlink(release_path, current_path)

    # Once, the build is uploaded to the remote,
    # set things up in the remote server.
    # Change directory to the release path.
    install_remote_dependencies(
        commit=commit,
        current_path=current_path,
        smart_install=get_stage_config(stage)['deployment']['smart_install']
    )

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
    notif.send(notification_types.DEPLOYMENT_FINISHED, notif_params)

    info('Deployment Completed')


def has_updated_dependencies(ref1, ref2):
    '''
    Check if dependencies for a node project has been updated
    in between the given two refs.
    '''
    changed_files = git.diff_files_between(ref1, ref2)

    # Check any of the npm/yarn files have changed
    # in between the two commits or refs.
    return (
        'package.json' in changed_files or
        'yarn.lock' in changed_files or
        'package-lock.json' in changed_files
    )


def install_remote_dependencies(commit, current_path, smart_install):
    ''' Install dependencies on the remote host. '''
    history = buildman.load_history()
    prev_build = buildman.get_prev_build_info(history)

    # Check if the installation could be skipped (smart_install).
    can_skip_installation = (
        smart_install and
        prev_build and
        not has_updated_dependencies(prev_build['commit'], commit)
    )

    # Smart install - copy the node_modules directory from the previous deployment
    # if it's usable (no dependencies or package manager files have changed).
    if can_skip_installation:
        runner.run(
            'cp -R {src} {dest}'.format(
                src=os.path.join(prev_build['path'], 'node_modules'),
                dest=os.path.join(current_path, 'node_modules')
            )
        )
        remote_info('Skipping installation - No change in dependencies.')
        return

    # Install dependencies on the remote.
    with cd(current_path):
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
