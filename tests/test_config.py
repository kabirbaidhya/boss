''' Unit tests for boss.config module. '''

from boss.constants import DEFAULT_CONFIG, PRESET_WEB
from boss.config import (
    merge_config,
    get_deployment_preset
)


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


def test_merge_config_that_by_default_cache_builds_is_true():
    '''
    Ensure build caching is turned on, i.e
    cache_build=True by default if not set.
    '''
    raw_config = {}
    merged_config = merge_config(raw_config)

    assert merged_config['deployment']['cache_builds'] is True


def test_merge_config_that_by_default_cache_builds_is_false_if_preset_web():
    '''
    Ensure build caching is turned off for web preset, i.e
    cache_build=False by default if not set.
    '''
    raw_config = {
        'deployment': {
            'preset': PRESET_WEB
        }
    }
    merged_config = merge_config(raw_config)

    assert merged_config['deployment']['cache_builds'] is False


def test_merge_config_that_default_config_values_are_put():
    '''
    Ensure default values are put if config options are not provided.
    '''
    raw_config = {}
    result = merge_config(raw_config)

    assert result['user'] == DEFAULT_CONFIG['user']
    assert result['port'] == DEFAULT_CONFIG['port']
    assert result['deployment'] == DEFAULT_CONFIG['deployment']


def test_merge_config_that_default_config_could_be_overridden():
    '''
    Ensure default config values could be overridden for the
    config options that are set, however the rest of the options
    that aren't set would still take default values.
    '''
    raw_config = {
        'port': '1234',
        'deployment': {
            'base_dir': '~/some/directory'
        }
    }
    result = merge_config(raw_config)

    assert result['port'] == raw_config['port']
    assert result['deployment']['base_dir'] == raw_config['deployment']['base_dir']

    # Not overridden, uses default values.
    assert result['user'] == DEFAULT_CONFIG['user']
    assert result['deployment']['preset'] == DEFAULT_CONFIG['deployment']['preset']
