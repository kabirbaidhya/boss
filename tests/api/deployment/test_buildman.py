''' Tests for boss.api.deployment.buildman module. '''

from mock import patch
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
