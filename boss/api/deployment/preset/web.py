# -*- coding: utf-8 -*-
'''
Web Deployment preset.

This would be useful for web projects and static files which needs to be deployed
to the remote server. This assumes the files are served via a web server eg: nginx, apache etc.
The source code is built locally and only the dist is uploaded and deployed to the server.
'''

from datetime import datetime

from fabric.api import task, cd

from boss.util import remote_info
from boss.api import shell, notif, fs, git, runner
from boss.config import get_stage_config, get as get_config
from boss.core.output import info
from boss.core.constants import notification_types, known_scripts
from .. import buildman


@task
def builds():
    ''' Display the build history. '''
    # Load the build history
    history = buildman.load_history()
    buildman.display_list(history)


@task
def rollback(id=None):
    ''' Zero-Downtime deployment rollback for the web. '''
    buildman.rollback(id)


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
    ''' Zero-Downtime deployment for the web. '''
    config = get_config()
    stage = shell.get_stage()
    user = get_stage_config(stage)['user']

    # Get the current branch and commit (locally).
    branch = git.current_branch(remote=False)
    commit = git.last_commit(remote=False, short=True)
    info('Deploying <{branch}:{commit}> to the {stage} server'.format(
        branch=branch,
        commit=commit,
        stage=stage
    ))

    tmp_path = fs.get_temp_filename()
    build_dir = buildman.resolve_local_build_dir()

    deploy_dir = buildman.get_deploy_dir()
    deployer_user = shell.get_user()

    notif.send(notification_types.DEPLOYMENT_STARTED, {
        'user': deployer_user,
        'branch': branch,
        'commit': commit,
        'stage': stage
    })

    runner.run_script_safely(known_scripts.PRE_DEPLOY)

    (release_dir, current_path) = buildman.setup_remote()

    timestamp = datetime.utcnow()
    build_id = timestamp.strftime('%Y%m%d%H%M%S')
    build_name = buildman.get_build_name(build_id)
    build_compressed = build_name + '.tar.gz'
    release_path = release_dir + '/' + build_name

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
