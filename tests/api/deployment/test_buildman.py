''' Tests for boss.api.deployment.buildman module. '''

import os
from mock import patch
from tempfile import mkstemp
from boss.core import fs
from boss.core.util.object import merge
from boss.core.constants.config import DEFAULT_CONFIG
from boss.api.deployment import buildman


@patch('boss.api.deployment.buildman.get_stage_config')
def test_resolve_local_build_dir_when_build_dir_is_configured(gsc_mock):
    '''
    Test resolve_local_build_dir() returns configured value if build_dir is configured.
    '''

    test_build_dir = 'my-build-directory'
    gsc_mock.return_value = {
        'deployment': {
            'build_dir': test_build_dir
        }
    }

    assert buildman.resolve_local_build_dir() == test_build_dir


@patch('os.path.exists')
@patch('boss.api.deployment.buildman.get_stage_config')
def test_resolve_local_build_dir_when_build_dir_is_none(gsc_mock, exists_mock):
    '''
    Test resolve_local_build_dir() returns one of the default
    build directories, if build_dir is not provided and
    fallback directories don't exist either.
    '''
    exists_mock.return_value = False
    gsc_mock.return_value = {
        'deployment': {
            'build_dir': None
        }
    }

    result = buildman.resolve_local_build_dir()

    assert result in buildman.LOCAL_BUILD_DIRECTORIES


@patch('os.path.exists')
@patch('boss.api.deployment.buildman.get_stage_config')
def test_resolve_local_build_dir_when_build_dir_none_with_fallback_directory(gsc_mock, exists_mock):
    '''
    Test resolve_local_build_dir(), when build_dir is not configured,
    but one of the fallback directories exist locally. It should return,
    the existing directory name.
    '''
    exists_mock.return_value = True
    gsc_mock.return_value = {
        'deployment': {
            'build_dir': None
        }

    }
    result = buildman.resolve_local_build_dir()

    assert result in buildman.LOCAL_BUILD_DIRECTORIES[0]


@patch('boss.api.deployment.buildman.load_history')
@patch('boss.api.deployment.buildman.git.last_commit')
def test_is_up_to_date_returns_true(glc_m, lh_m):
    ''' Test is_up_to_date(). '''
    glc_m.return_value = '5ff8648'
    lh_m.return_value = {
        'builds': [
            {'id': '1', 'commit': '1232333'},
            {'id': '2', 'commit': '5ff8648'}
        ],
        'current': '2'
    }

    assert buildman.is_remote_up_to_date()


@patch('boss.api.deployment.buildman.load_history')
@patch('boss.api.deployment.buildman.git.last_commit')
def test_is_up_to_date_returns_false(glc_m, lh_m):
    ''' Test is_up_to_date(). '''
    glc_m.return_value = '5ff8648'
    lh_m.return_value = {
        'builds': [
            {'id': '1', 'commit': '1255452'},
            {'id': '2', 'commit': '1232333'}
        ],
        'current': '2'
    }

    assert not buildman.is_remote_up_to_date()


def test_get_prev_build_info():
    ''' Test get_prev_build_info() returns previous build information. '''
    history = {
        'builds': [
            {'id': 'abc0', 'commit': '1255452', 'path': '/home/kabir/builds/test1'},
            {'id': 'abc1', 'commit': '1232333', 'path': '/home/kabir/builds/test2'}
        ],
        'current': 'abc0'
    }

    prev_build = buildman.get_prev_build_info(history)

    assert prev_build == history['builds'][1]


def test_get_prev_build_info_if_no_previous_build():
    ''' Test get_prev_build_info() returns None if previous build does not exist. '''
    history = {
        'builds': [
            {'id': 'abc0', 'commit': '1255452', 'path': '/home/kabir/builds/test1'},
            {'id': 'abc1', 'commit': '1232333', 'path': '/home/kabir/builds/test2'}
        ],
        'current': 'abc1'
    }

    prev_build = buildman.get_prev_build_info(history)

    assert prev_build is None


def test_get_prev_build_info_if_empty_history():
    ''' Test get_prev_build_info() returns None if history is empty. '''
    history = {}
    prev_build = buildman.get_prev_build_info(history)

    assert prev_build is None


def test_get_prev_build_info_if_empty_builds_or_current():
    '''
    Test get_prev_build_info() returns None if
    build history is empty or current is None.
    '''
    history = {
        'builds': [],
        'current': None
    }
    prev_build = buildman.get_prev_build_info(history)

    assert prev_build is None


@patch('boss.api.deployment.buildman.load_remote_env_vars')
@patch('boss.api.runner._get_config')
def test_build_with_loaded_env_vars(get_config_m, remote_env_m, capfd):
    '''
    Test build() with env vars injected from remote path and vault.

    Precedence:
        - Env vars injected from OS
        - Env vars injected by boss (eg: STAGE=stage)
        - Env vars injected from remote (remote_env_path if remote_env_injection = True)
        - Env vars injected from vault
    '''

    build_script = '''
    echo STAGE = $STAGE
    echo FOO = $FOO
    echo BAR = $BAR
    echo BAT = $BAT
    echo BAZ = $BAZ
    '''

    (_, script_path) = mkstemp()
    fs.write(script_path, build_script)
    test_config = merge(DEFAULT_CONFIG, {
        'remote_env_injection': True,
        'stages': {
            'stage1': {
                'remote_env_path': 'remote/env/path',
            }
        },
        'scripts': {
            'build': 'sh ' + script_path
        }
    })
    get_config_m.return_value = test_config
    remote_env_m.return_value = {
        'BAR': 'bar-from-remote',
        'BAT': 'bat-from-remote'
    }
    # Injected from host os
    os.environ['FOO'] = 'foo-from-host'

    # Vault's env vars are injected into the Host's env
    os.environ['BAT'] = 'bat-from-vault'
    os.environ['BAZ'] = 'baz-from-vault'

    buildman.build('stage1', test_config)

    out, _ = capfd.readouterr()

    # Assert all the environment varialbes have been injected
    # in the build script
    assert 'STAGE = stage1' in out
    assert 'FOO = foo-from-host' in out
    assert 'BAR = bar-from-remote' in out
    assert 'BAT = bat-from-vault' in out
    assert 'BAZ = baz-from-vault' in out
