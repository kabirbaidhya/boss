# -*- coding: utf-8 -*-
'''
Build Manager for deployment.
'''

import json

from terminaltables import SingleTable
from fabric.colors import green
from fabric.api import cd, hide

from boss import __version__ as BOSS_VERSION
from boss.config import get as get_config
from boss.util import remote_info, merge
from boss.api import fs

BUILD_NAME_FORMAT = 'build-{id}'
INITIAL_BUILD_HISTORY = {
    'bossVersion': BOSS_VERSION,
    'preset': None,
    'current': None,
    'builds': []
}
BUILDS_DIRECTORY = '/builds'
BUILDS_META_FILE = '/builds.json'


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


def load_history():
    ''' Load build history. '''
    with hide('everything'):
        data = fs.read_remote_file(get_builds_file())

        return json.loads(data)


def save_history(data):
    ''' Save build history. '''
    fs.save_remote_file(get_builds_file(), json.dumps(data))


def display(id):
    ''' Display build information by build id. '''
    history = load_history()
    build = get_build_info(history, id or history['current'])
    is_current = build['id'] == history['current']

    table = SingleTable([
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


def setup_remote():
    ''' Setup remote environment before we can proceed with the deployment process. '''
    base_dir = get_deploy_dir()
    release_dir = get_release_dir()
    current_path = base_dir + '/current'
    build_history_path = get_builds_file()
    preset = get_config()['deployment']['preset']

    # If the release directory does not exist, create it.
    if not fs.exists(release_dir):
        remote_info('Creating the releases directory {}'.format(release_dir))
        fs.mkdir(release_dir, nested=True)

    # If the build history file does not exist, create it now.
    if not fs.exists(build_history_path):
        remote_info(
            'Creating new build history file {}'.format(build_history_path)
        )
        save_history(merge(INITIAL_BUILD_HISTORY, {
            'preset': preset
        }))

    return (release_dir, current_path)


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


def record_build_history(build_info):
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
