''' Unit tests for boss.config module. '''

from mock import patch
from boss.core.util.string import strip_ansi
from boss.core.constants.config import DEFAULT_CONFIG
from boss.config import (
    load,
    merge_config,
    resolve_dotenv_file,
    get_deployment_preset
)


SAMPLE_BOSS_YAML = '''
project_name: test-project
user: test-user
deployment:
    preset: web
    base_dir: ~/source/deployment
'''


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
    assert result['deployment']['base_dir'] == raw_config[
        'deployment']['base_dir']

    # Not overridden, uses default values.
    assert result['user'] == DEFAULT_CONFIG['user']
    assert result['deployment'][
        'preset'] == DEFAULT_CONFIG['deployment']['preset']


def test_merge_config_base_config_is_merged_to_each_stage_specfic_config():
    '''
    Ensure the base deployment config and basic config are merged to
    each of the stage configurations
    '''
    raw_config = {
        'port': '1234',
        'remote_env_path': 'test',
        'deployment': {
            'base_dir': '~/some/directory'
        },
        'stages': {
            'stage1': {
                'host': 'stage1.example.com',
                'remote_env_path': 'best'
            },
            'stage2': {
                'host': 'stage2.example.com',
                'port': '4321'
            }
        }
    }
    result = merge_config(raw_config)

    # Stage1
    stage1_config = result['stages']['stage1']
    assert stage1_config['port'] == raw_config['port']
    assert stage1_config['host'] == raw_config['stages']['stage1']['host']
    assert stage1_config['remote_env_path'] == raw_config['stages']['stage1']['remote_env_path']
    assert stage1_config['deployment'][
        'base_dir'] == raw_config['deployment']['base_dir']
    assert stage1_config['deployment'][
        'build_dir'] == DEFAULT_CONFIG['deployment']['build_dir']

    # Stage 2
    stage2_config = result['stages']['stage2']
    assert stage2_config['port'] == raw_config['stages']['stage2']['port']
    assert stage2_config['host'] == raw_config['stages']['stage2']['host']
    assert stage2_config['remote_env_path'] == raw_config['remote_env_path']
    assert stage2_config['deployment'][
        'base_dir'] == raw_config['deployment']['base_dir']
    assert stage2_config['deployment'][
        'build_dir'] == DEFAULT_CONFIG['deployment']['build_dir']


@patch('boss.core.fs.read')
def test_load(read_mock):
    ''' Test load() function loads yaml file correctly. '''
    read_mock.return_value = SAMPLE_BOSS_YAML
    config_filename = 'test.yml'
    boss_config = load(config_filename)

    read_mock.assert_called_with(config_filename)

    # Configured options
    assert boss_config['user'] == 'test-user'
    assert boss_config['project_name'] == 'test-project'
    assert boss_config['deployment']['preset'] == 'web'
    assert boss_config['deployment']['base_dir'] == '~/source/deployment'

    # Default values resolved
    assert boss_config['port'] == 22
    assert boss_config['port'] == 22


@patch('boss.config.info')
@patch('dotenv.load_dotenv')
def test_resolve_dotenv_file_loads_dotenv_file_if_it_exists(load_dotenv_mock, info_m):
    ''' Test .env file is loaded if it exists. '''
    dotenv_path = '.env'

    with patch('boss.core.fs.exists', side_effect=lambda p: p == dotenv_path):
        resolve_dotenv_file('')
        load_dotenv_mock.assert_called_with(dotenv_path)
        msg = strip_ansi(info_m.call_args[0][0])

        assert msg == 'Resolving env file: .env'


@patch('boss.config.info')
@patch('boss.core.fs.exists')
@patch('dotenv.load_dotenv')
def test_resolve_dotenv_file_is_not_loaded_if_not_exists(load_dotenv_m, exists_m, _):
    ''' Test .env file is not loaded if it doesn't exists. '''
    exists_m.return_value = False
    resolve_dotenv_file('')
    load_dotenv_m.assert_not_called()


@patch('boss.config.info')
@patch('dotenv.load_dotenv')
def test_resolve_dotenv_file_loads_stage_specific_env_file(load_dotenv_m, info_m):
    ''' Test .env file is loaded if it exists. '''
    stage = 'production'

    def exists(p):
        return p == '.env.production'

    with patch('boss.core.fs.exists', side_effect=exists):
        resolve_dotenv_file('', stage)
        load_dotenv_m.assert_called_with('.env.production')
        msg = strip_ansi(info_m.call_args[0][0])

        assert msg == 'Resolving env file: .env.production'


@patch('boss.config.info')
@patch('dotenv.load_dotenv')
def test_resolve_dotenv_file_loads_env_file_if_stage_specific_file_doesnt_exist(
        load_dotenv_m, info_m):
    '''
    Test .env file is loaded as a fallback option,
    if stage is provided but stage specific env file doesn't exist.
    '''

    stage = 'production'

    def exists(p):
        return p == '.env'

    with patch('boss.core.fs.exists', side_effect=exists):
        resolve_dotenv_file('', stage)
        load_dotenv_m.assert_called_with('.env')

        msg = strip_ansi(info_m.call_args[0][0])

        assert msg == 'Resolving env file: .env'
