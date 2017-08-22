# -*- coding: utf-8 -*-
'''
Frontend Deployment preset.

This would be useful for frontend projects and static files which needs to be deployed
to the remote server. This assumes the files are served via a web server eg: nginx, apache etc.
The source code is built locally and only the dist is uploaded and deployed to the server.
'''

from datetime import datetime

from fabric.colors import cyan
from fabric.api import task, cd, shell_env

from boss import constants
from boss.util import info, remote_info, echo
from boss.api import shell, notif, runner, hipchat, fs, git
from boss.config import get_stage_config, get as get_config
from . import buildman


@task
def builds():
    ''' Display the build history. '''
    # Load the build history
    history = buildman.load_history()
    buildman.display_list(history)


@task
def rollback(id=None):
    ''' Zero-Downtime deployment rollback for the frontend. '''
    # TODO: Send rollback started notification
    config = get_config()
    stage = shell.get_stage()
    (_, current_path) = buildman.setup_remote()
    history = buildman.load_history()

    # If the current build in the history is not set yet or
    # there aren't any previous builds on the history
    # rollback is not possible.
    if not history['current'] or not history['builds']:
        remote_info('Could not get the previous build to rollback.')
        return

    if not id:
        # If the rollback build id is not explicitly provided,
        # get the previous build of the current build.
        current_index = buildman.get_current_build(history, index=True)

        # If current_index is None, or there are no builds before the current build
        # print the error since there are no previous builds to rollback.
        build_count = len(history['builds'])
        has_prev_build = 0 < current_index + 1 < build_count

        if current_index is None or not has_prev_build:
            remote_info('No previous builds found to rollback.')
            return

        # Get the previous build information.
        prev_build = history['builds'][current_index + 1]
    else:
        # Otherwise, if the id is provided then, get the build with that id
        prev_build = buildman.get_build_by_id(history, id)

        if not prev_build:
            remote_info('Build with id "{}" not found.'.format(id))
            return

    remote_info('Rolling back to build {}'.format(prev_build['id']))
    fs.update_symlink(prev_build['path'], current_path)
    history['current'] = prev_build['id']

    # Save the build history
    buildman.save_history(history)

    # Display the updated builds.
    buildman.display_list(history)

    stage_config = get_stage_config(stage)

    # Send rollback completed notification.
    send_rollback_notification({
        'project_name': config['project_name'],
        'repository_url': config['repository_url'],
        'server_name': stage,
        'build': prev_build['id'],
        'user': shell.get_user(),
        'public_url': stage_config['public_url'],
    })
    remote_info('Rollback successful')


@task
def buildinfo(id=None):
    ''' Print the build information. '''
    buildman.display(id)


@task
def deploy():
    ''' Zero-Downtime deployment for the frontend. '''
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
    build_name = buildman.BUILD_NAME_FORMAT.format(id=build_id)
    build_compressed = build_name + '.tar.gz'
    release_path = release_dir + '/' + build_name

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
        fs.mkdir(build_name)

        # Extract the build.
        fs.tar_extract(tmp_path, build_name)

        # Remove the uploaded archived from the temp path.
        fs.rm_rf(tmp_path)

        remote_info(
            'Changing ownership of {} to user {}'.format(deploy_dir, user)
        )
        fs.chown(release_path, user, user)

        remote_info('Pointing the current symlink to the latest build')
        fs.update_symlink(release_path, current_path)

    # Save build history
    buildman.record_build_history({
        'id': build_id,
        'path': release_path,
        'branch': branch,
        'commit': commit,
        'stage': stage,
        'createdBy': deployer_user,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S (UTC)')
    })

    # Send deployment finished notification.
    notif.send(notif.DEPLOYMENT_FINISHED, {
        'branch': branch,
        'stage': stage
    })

    remote_info('Deployment Completed')


def send_rollback_notification(params):
    ''' Send notification about the rollback process. '''
    config = get_config()

    # Notify on hipchat
    if hipchat.is_enabled():
        hipchat_config = config['notifications']['hipchat']
        project_link = hipchat.create_link(
            params['repository_url'],
            params['project_name']
        )

        server_short_link = hipchat.create_link(
            params['public_url'], params['server_name']
        )
        message = '{user} rolled back {project_link} deployment on {server_link} server to build {build}.'
        text = message.format(
            user=params['user'],
            build=params['build'],
            project_link=project_link,
            server_link=server_short_link
        )

        hipchat.notify({
            'color': hipchat_config['deployed_color'],
            'message': text,
            'notify': hipchat_config['notify'],
            'message_format': 'html'
        })
