# -*- coding: utf-8 -*-
'''
Build Manager for deployment.
'''
import os
import json
import time
from datetime import datetime

from terminaltables import SingleTable
from fabric.api import cd, hide, shell_env

from boss import BASE_PATH, __version__ as BOSS_VERSION
from boss.config import get as get_config, get_stage_config
from boss.util import remote_info, remote_print
from boss.api import fs, shell, runner
from boss.core import env
from boss.core.util import ts
from boss.core.output import info
from boss.core.util.object import merge
from boss.core.util.colors import green, cyan
from boss.core.constants import presets, known_scripts

LOCAL_BUILD_DIRECTORIES = ['build/', 'dist/']
INITIAL_BUILD_HISTORY = {
    'bossVersion': BOSS_VERSION,
    'preset': None,
    'current': None,
    'builds': []
}
BUILDS_DIRECTORY = '/builds'
BUILDS_META_FILE = '/builds.json'
CURRENT_BUILD_LINK = '/current'
DEFAULT_HTML_PATH = '/default_html'
TS_FORMAT = '%Y-%m-%d %H:%M:%S (UTC)'
TS_FORMAT_LOCAL = '%Y-%m-%d %I:%M:%S %p'


def get_deploy_dir():
    ''' Get the deployment base directory path. '''
    config = get_stage_config(shell.get_stage())

    return config['deployment']['base_dir'].rstrip('/')


def resolve_local_build_dir():
    '''
    Get the local build directory and verify if it exists locally.
    Throws and error if the build directory doesn't exist.
    '''
    config = get_stage_config(shell.get_stage())
    build_dir = config['deployment']['build_dir']

    # If build_dir is configured, just return it.
    if build_dir:
        return build_dir

    # Look up for fallback local directories, if build_dir isn't provided.
    for folder in LOCAL_BUILD_DIRECTORIES:
        if os.path.exists(folder):
            return folder

    # If fallback directories don't exist either,
    # return one of the default build directories.
    return LOCAL_BUILD_DIRECTORIES[0]


def get_release_dir():
    ''' Get the builds base directory path. '''
    return get_deploy_dir() + BUILDS_DIRECTORY


def get_current_path():
    ''' Get the current path. '''
    return get_deploy_dir() + CURRENT_BUILD_LINK


def get_builds_file():
    ''' Get the build metadata file. '''
    return get_deploy_dir() + BUILDS_META_FILE


def get_build_name(id):
    ''' Get build name using id. '''
    return 'build-{id}'.format(id=id)


def load_history():
    ''' Load build history. '''
    with hide('everything'):
        data = fs.read_remote_file(get_builds_file())

        return json.loads(data)


def save_history(data):
    ''' Save build history. '''
    fs.save_remote_file(get_builds_file(), json.dumps(data))


def local_timestamp(timestamp, tz=True):
    '''
    Get the corresponding local timestamp for the
    UTC timestamp stored in the server.
    '''
    timestamp_utc = datetime.strptime(timestamp, TS_FORMAT)
    timestamp_local = ts.localize_utc_timestamp(timestamp_utc)

    tz_name = time.strftime(' (%Z)') if tz else ''
    return timestamp_local.strftime(TS_FORMAT_LOCAL) + tz_name


def display(id):
    ''' Display build information by build id. '''
    history = load_history()
    build = get_build_info(history, id or history['current'])
    is_current = build['id'] == history['current']
    timestamp = local_timestamp(build['timestamp'])

    table = SingleTable([
        [green('Build ' + build['id'])],
        ['ID: ' + green(build['id'])],
        ['Commit: ' + green(build['commit'])],
        ['Branch: ' + green(build['branch'])],
        ['Stage: ' + green(build['stage'])],
        ['Created By: ' + green(build['createdBy'])],
        ['Path: ' + green(build['path'])],
        ['Current Build: ' + green('Yes' if is_current else 'No')],
        ['Timestamp: ' + green(timestamp)]
    ])
    print(table.table)


def display_list(history):
    ''' Display build history. '''
    if not history['builds']:
        remote_info('No builds have been deployed yet.')
        return

    remote_info('Showing recent builds')

    # Map build data into tabular format
    data = map(row_mapper_wrt(history['current']), history['builds'])

    # Prepend heading rows
    data.insert(0, [
        ' ', 'ID', 'Commit',
        'Branch', 'Created By', 'Timestamp'
    ])

    table = SingleTable(data)
    print('')
    print(table.table)


def row_mapper_wrt(current):
    ''' Returns a mapper with respect to the current row. '''
    def mapper(data):
        ''' Maps build information to a tabular row. '''
        is_current = data['id'] == current
        pointer = u'➜' if is_current else ' '
        timestamp = local_timestamp(data['timestamp'])

        row = [
            pointer, data['id'], data['commit'],
            data['branch'], data['createdBy'], timestamp
        ]

        # Regular row if not a current build row.
        if not is_current:
            return row

        # Return colored row, if it's the current build row.
        return map(green, row)

    return mapper


def is_remote_setup():
    ''' Check if the remote is setup for deployment. '''
    release_dir = get_release_dir()
    return fs.exists(release_dir)


def setup_remote(quiet=True):
    ''' Setup remote environment before we can proceed with the deployment process. '''
    base_dir = get_deploy_dir()
    release_dir = get_release_dir()
    current_path = get_current_path()
    build_history_path = get_builds_file()
    preset = get_config()['deployment']['preset']
    did_setup = False
    stage = shell.get_stage()

    # If the release directory does not exist, create it.
    if not fs.exists(release_dir):
        remote_info(
            'Setting up {} server for {} deployment'.format(stage, preset)
        )
        remote_info(
            'Creating the releases directory {}'.format(cyan(release_dir))
        )
        fs.mkdir(release_dir, nested=True)

        # Add build history file.
        remote_info(
            'Creating new build meta file {}'.format(cyan(build_history_path))
        )
        save_history(merge(INITIAL_BUILD_HISTORY, {'preset': preset}))

        # Setup a default web page for web deployment.
        if preset == presets.WEB:
            setup_default_html(base_dir)

        did_setup = True

    if not did_setup and not quiet:
        remote_info('Remote already setup for deployment')

    return (release_dir, current_path)


def setup_default_html(base_dir):
    ''' Setup default html web page on the remote host. '''
    current_path = base_dir + CURRENT_BUILD_LINK
    html_path = BASE_PATH + '/misc/default_html'
    remote_html_path = base_dir + DEFAULT_HTML_PATH

    remote_info('Setting up the default web page')
    fs.upload_dir(html_path, base_dir)

    # Point the current sym link to the default web page.
    fs.update_symlink(remote_html_path, current_path)

    remote_info('Remote is setup and is ready for deployment.')
    remote_print((
        'Deployed build will point to {0}.\n' +
        'For serving the latest build, ' +
        'please set your web server document root to {0}.'
    ).format(cyan(current_path)))


def delete_old_builds(history):
    ''' Auto delete unnecessary build directories from the filesystem. '''
    build_path = get_release_dir()
    kept_builds = map(lambda x: get_build_name(x['id']), history['builds'])
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


def record_history(build_info):
    ''' Record a new build in the history. '''
    config = get_config()
    keep_builds = int(config['deployment']['keep_builds'])
    build_history = load_history()

    build_history['current'] = build_info['id']
    build_history['builds'].insert(0, build_info)
    build_history['builds'] = build_history['builds'][0:keep_builds]

    remote_info('Saving the build history')

    # Update build history json file
    save_history(build_history)

    # Delete the previous builds more than the value of `keep_builds`.
    delete_old_builds(build_history)


def get_current_build_index(history):
    ''' Get the current build index. '''
    if not history['current']:
        remote_info('No current build found.')
        return None

    # Return the build index for the current build.
    current = history['current']
    for i, build in enumerate(history['builds']):
        if build['id'] == current:
            return i

    return None


def get_build_by_id(history, id):
    return next((x for x in history['builds'] if x['id'] == id), None)


def get_build_info(history, id):
    ''' Get the build information by build id. '''

    if not history['builds']:
        remote_info('No build history recorded yet.')
        return None

    return get_build_by_id(history, id)


def rollback(id=None):
    '''
    Deployment rollback to the previous build, or
    the build identified by the given id.
    '''
    # TODO: Send rollback started notification
    (_, current_path) = setup_remote()
    history = load_history()

    # If the current build in the history is not set yet or
    # there aren't any previous builds on the history
    # rollback is not possible.
    if not history['current'] or not history['builds']:
        remote_info('Could not get the previous build to rollback.')
        return

    # If the rollback build id is not explicitly provided,
    # rollback to the previous build.
    if not id:
        current_index = get_current_build_index(history)

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
        prev_build = get_build_by_id(history, id)

        if not prev_build:
            remote_info('Build with id "{}" not found.'.format(id))
            return

    remote_info('Rolling back to build {}'.format(prev_build['id']))
    fs.update_symlink(prev_build['path'], current_path)

    # Save history and display it.
    history['current'] = prev_build['id']
    save_history(history)
    display_list(history)

    # TODO: Send rollback completed notification.
    remote_info('Rollback successful')


def load_remote_env_vars(remote_env_path):
    '''
    Load remote env variables and return them as
    key-value pairs (dict) of environment variables.
    '''
    env_def = fs.read_remote_file(remote_env_path)
    env_vars = env.parse(env_def)

    return env_vars


def get_build_env_vars(stage, config):
    ''' Get env vars to be injected to the build script. '''
    # The stage for which the build script is being run is passed
    # via an environment variable STAGE.
    # This could be useful for creating specific builds for
    # different environments.
    env_vars = merge(os.environ, {
        'STAGE': stage
    })

    # If remote env injection is not enabled skip it.
    if not config['remote_env_injection']:
        return env_vars

    # Remote environment variables are sent to the build script too
    # if remote_env_injection is enabled.
    remote_env_path = config['stages'][stage]['remote_env_path']
    remote_vars = load_remote_env_vars(remote_env_path)

    return merge(remote_vars, env_vars)


def build(stage, config):
    '''
    Trigger build script to prepare a build for the given stage.
    '''
    info('Getting the build ready for deployment')

    # Trigger the install script
    runner.run_script_safely(known_scripts.PRE_INSTALL, remote=False)
    runner.run_script_safely(known_scripts.INSTALL, remote=False)
    runner.run_script_safely(known_scripts.POST_INSTALL, remote=False)

    env_vars = get_build_env_vars(stage, config)

    with shell_env(**env_vars):
        runner.run_script_safely(known_scripts.PRE_BUILD, remote=False)
        runner.run_script_safely(known_scripts.BUILD, remote=False)
        runner.run_script_safely(known_scripts.POST_BUILD, remote=False)
