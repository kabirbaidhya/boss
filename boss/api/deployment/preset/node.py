# -*- coding: utf-8 -*-
'''
Node Application Deployment preset.

This would be useful for deploying node js projects to the remote server.
Here the source is built locally and uploaded to the server, then the application service
is started on restarted on the remote server.
'''

from datetime import datetime

from fabric.colors import cyan
from fabric.api import task, cd, shell_env

from boss import constants
from boss.util import info, remote_info, echo
from boss.api import shell, notif, runner, fs, git
from boss.config import get as get_config
from .. import buildman

NODE_INCLUDE_FILES = ['package.json', 'yarn.lock', 'package-lock.json']


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


@task(alias='info')
def buildinfo(id=None):
    ''' Print the build information. '''
    buildman.display(id)


@task
def setup():
    ''' Setup remote host for deployment. '''
    buildman.setup_remote(quiet=False)


def upload_included_files(remote_path):
    ''' Upload the local files if they were to be included. '''
    for filename in NODE_INCLUDE_FILES:
        # Skip upload if the file doesn't exist.
        if not fs.exists(filename, remote=False):
            continue

        fs.upload(filename, remote_path)


@task
def deploy():
    ''' Zero-Downtime deployment for the backend. '''
    config = get_config()
    user = config['user']
    stage = shell.get_stage()

    info('Deploying app to the {} server'.format(stage))
    # Get the current branch and commit (locally).
    branch = git.current_branch(remote=False)
    commit = git.last_commit(remote=False)

    echo('  Branch: {}'.format(cyan(branch)))
    echo('  Commit: {}'.format(cyan(commit)))

    tmp_path = fs.get_temp_filename()
    build_dir = config['deployment']['build_dir']

    deploy_dir = buildman.get_deploy_dir()
    deployer_user = shell.get_user()

    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': deployer_user,
        'branch': branch,
        'stage': stage
    })

    (release_dir, current_path) = buildman.setup_remote()

    timestamp = datetime.utcnow()
    build_id = timestamp.strftime('%Y%m%d%H%M%S')
    build_name = buildman.get_build_name(build_id)
    build_compressed = build_name + '.tar.gz'
    release_path = release_dir + '/' + build_name
    dist_path = build_name + '/dist'

    info('Getting the build ready for deployment')

    # Trigger the install script
    runner.run_script(constants.SCRIPT_INSTALL, remote=False)

    # Trigger the build script.
    #
    # The stage for which the build script is being run is passed
    # via an environment variable STAGE.
    # This could be useful for creating specific builds for
    # different environments.
    with shell_env(STAGE=stage):
        runner.run_script(constants.SCRIPT_BUILD, remote=False)

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
        upload_included_files(release_path)

        remote_info('Pointing the current symlink to the latest build')
        fs.update_symlink(release_path, current_path)

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

    # Send deployment finished notification.
    notif.send(notif.DEPLOYMENT_FINISHED, {
        'branch': branch,
        'stage': stage
    })

    remote_info('Deployment Completed')
