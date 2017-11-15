''' Tests for boss.api.deployment.buildman module. '''

from mock import patch


@patch('boss.config.get_stage_config')
def test_resolve_local_build_dir_when_build_dir_is_configured(stage_config_mock):
    '''
    Test resolve_local_build_dir() returns configured value if build_dir is configured.
    '''

    from boss.api.deployment import buildman

    test_build_dir = 'my-build-directory'
    stage_config_mock.return_value = {
        'deployment': {
            'build_dir': test_build_dir
        }
    }

    assert buildman.resolve_local_build_dir() == test_build_dir
