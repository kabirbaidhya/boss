# -*- coding: utf-8 -*-
'''
Frontend Deployment preset.

This would be useful for frontend projects and static files which needs to be deployed
to the remote server. This assumes the files are served via a web server eg: nginx, apache etc.
The source code is built locally and only the dist is uploaded and deployed to the server.
'''

import json
from datetime import datetime

from terminaltables import AsciiTable
from fabric.colors import green, cyan
from fabric.api import task, cd, shell_env, hide

from boss import constants, __version__ as BOSS_VERSION
from boss.util import info, remote_info, echo
from boss.api import shell, notif, runner, hipchat, fs, git
from boss.config import get_stage_config, get as get_config

BUILD_NAME_FORMAT = 'build-{id}'
INITIAL_BUILD_HISTORY = {
    'bossVersion': BOSS_VERSION,
    'current': None,
    'builds': []
}
BUILDS_DIRECTORY = '/builds'
BUILDS_META_FILE = '/builds.json'


def setup_remote():
    ''' Setup remote environment before we can proceed with the deployment process. '''
    base_dir = get_deploy_dir()
    release_dir = get_release_dir()
    current_path = base_dir + '/current'
    build_history_path = get_builds_file()

    # If the release directory does not exist, create it.
    if not fs.exists(release_dir):
        remote_info('Creating the releases directory {}'.format(release_dir))
        fs.mkdir(release_dir, nested=True)

    # If the build history file does not exist, create it now.
    if not fs.exists(build_history_path):
        remote_info(
            'Creating new build history file {}'.format(build_history_path)
        )
        save_build_history(INITIAL_BUILD_HISTORY)

    return (release_dir, current_path)


def get_deploy_dir():
    ''' Get the deployment base directory path. '''
    config = get_config()
    return config['deployment']['base_dir'].rstrip('/')


def get_release_dir():
    ''' Get the builds base directory path. '''
    return get_deploy_dir() + BUILDS_DIRECTORY


def get_builds_file():
    ''' Get the build metadata file. '''
    return get_deploy_dir() + BUILDS_META_FILE


@task
def builds():
    ''' Display the build history. '''
    # Load the build history
    history = load_build_history()

    if not history['builds']:
        remote_info('No builds have been deployed yet.')
        return

    # Map build data into tabular format
    data = map(row_mapper_wrt(history['current']), history['builds'])

    # Prepend heading rows
    data.insert(0, [
        ' ', 'ID', 'Commit',
        'Branch', 'Created By', 'Timestamp'
    ])

    table = AsciiTable(data)
    print(table.table)


def row_mapper_wrt(current):
    ''' Returns a mapper with respect to the current row. '''
    def mapper(data):
        ''' Maps build information to a tabular row. '''
        is_current = data['id'] == current
        pointer = u'➜' if is_current else ' '

        row = [
            pointer, data['id'], data['commit'],
            data['branch'], data['createdBy'], data['timestamp']
        ]

        # Regular row if not a current build row.
        if not is_current:
            return row

        # Return colored row, if it's the current build row.
        return map(green, row)

    return mapper


def load_build_history():
    ''' Load build history. '''
    with hide('everything'):
        data = fs.read_remote_file(get_builds_file())

        return json.loads(data)


def save_build_history(data):
    ''' Save build history. '''
    fs.save_remote_file(get_builds_file(), json.dumps(data))


def record_build_history(build_info):
    ''' Record a new build in the history. '''
    config = get_config()
    keep_builds = int(config['deployment']['keep_builds'])
    build_history = load_build_history()

    build_history['current'] = build_info['id']
    build_history['builds'].insert(0, build_info)
    build_history['builds'] = build_history['builds'][0:keep_builds]

    remote_info('Saving the build history')

    # Update build history json file
    save_build_history(build_history)

    # Delete the previous builds more than the value of `keep_builds`.
    delete_old_builds(build_history)


def get_current_build(history, index=False):
    ''' Get the current build information. '''
    if not history['current']:
        remote_info('No current build found.')
        return None

    return get_build_info(history, history['current'], index)


def get_build_by_id(history, id):
    return next((x for x in history['builds'] if x['id'] == id), None)


def get_build_info(history, id, index=False):
    ''' Get the build information by build id. '''

    if not history['builds']:
        remote_info('No build history recorded yet.')
        return None

    # If index is not requested, return the build information instead.
    if not index:
        return get_build_by_id(history, id)

    # Return the build index.
    return next((i for i, x in enumerate(history['builds']) if x['id'] == id), None)


@task
def rollback(id=None):
    ''' Zero-Downtime deployment rollback for the frontend. '''
    # TODO: Send rollback started notification
    config = get_config()
    stage = shell.get_stage()
    (_, current_path) = setup_remote()
    history = load_build_history()

    # If the current build in the history is not set yet or
    # there aren't any previous builds on the history
    # rollback is not possible.
    if not history['current'] or not history['builds']:
        remote_info('Could not get the previous build to rollback.')
        return

    if not id:
        # If the rollback build id is not explicitly provided,
        # get the previous build of the current build.
        current_index = get_current_build(history, index=True)

        # If current_index is None, or there are no builds before the current build
        # print the error since there are no previous builds to rollback.
        if current_index is None or not history['builds'][current_index + 1]:
            remote_info('No previous builds found to rollback.')
            return

        # Get the previous build information.
        prev_build = history['builds'][current_index + 1]
    else:
        # Otherwise, if the id is provided then, get the build with that id
        prev_build = get_build_by_id(history, id)

        if not prev_build:
            remote_info('Build with id "{}" not found.'.format(id))
            return

    remote_info('Rolling back to build {}'.format(prev_build['id']))
    fs.update_symlink(prev_build['path'], current_path)
    history['current'] = prev_build['id']
    save_build_history(history)

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
    history = load_build_history()
    build = get_build_info(history, id or history['current'])
    is_current = build['id'] == history['current']

    table = AsciiTable([
        [green('Build ' + build['id'])],
        ['ID: ' + green(build['id'])],
        ['Commit: ' + green(build['commit'])],
        ['Branch: ' + green(build['branch'])],
        ['Stage: ' + green(build['stage'])],
        ['Created By: ' + green(build['createdBy'])],
        ['Path: ' + green(build['path'])],
        ['Current Build: ' + green('Yes' if is_current else 'No')],
        ['Timestamp: ' + green(build['timestamp'])]
    ])
    print(table.table)


def delete_old_builds(history):
    ''' Auto delete unnecessary build directories from the filesystem. '''
    build_path = get_release_dir()
    kept_builds = [BUILD_NAME_FORMAT.format(id=x['id'])
                   for x in history['builds']]
    found_builds = fs.glob(build_path)
    to_be_deleted_builds = [x for x in found_builds if x not in kept_builds]
    deletion_count = len(to_be_deleted_builds)

    # Skip, if there are no builds to be deleted.
    if deletion_count == 0:
        return

    # Remove directories to be deleted.
    with cd(build_path):
        fs.rm_rf(to_be_deleted_builds)
        remote_info(
            'Deleted {} old build(s) from the remote'.format(deletion_count)
        )


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

    deploy_dir = get_deploy_dir()
    deployer_user = shell.get_user()

    notif.send(notif.DEPLOYMENT_STARTED, {
        'user': deployer_user,
        'branch': branch,
        'stage': stage
    })

    (release_dir, current_path) = setup_remote()

    timestamp = datetime.utcnow()
    build_id = timestamp.strftime('%Y%m%d%H%M%S')
    build_name = BUILD_NAME_FORMAT.format(id=build_id)
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
    record_build_history({
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
    # TODO: This logic should go to boss-cli too.
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
