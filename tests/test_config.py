''' Unit tests for boss.config module. '''

from boss.config import get_deployment_preset, DEFAULT_CONFIG


def test_get_deployment_preset_returns_configured_preset():
    '''
    Check get_deployment_preset() function returns
    the configured deployment preset if it is configured.
    '''
    raw_config = {
        'deployment': {
            'preset': 'test-preset'
        }
    }
    preset = get_deployment_preset(raw_config)

    assert preset == 'test-preset'


def test_get_deployment_preset_returns_default_preset_if_not_set():
    '''
    Check get_deployment_preset() function returns,
    the default deployment preset if it is not configured.
    '''
    raw_config = {
        'project_name': 'test-project'
    }
    preset = get_deployment_preset(raw_config)

    assert preset == DEFAULT_CONFIG['deployment']['preset']
