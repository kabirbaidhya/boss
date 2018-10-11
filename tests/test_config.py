''' Unit tests for boss.config module. '''

import os
from mock import patch
from boss.core.util.string import strip_ansi
from boss.core.constants.config import DEFAULT_CONFIG
from boss.config import (
    load,
    parse_config,
    merge_config,
    is_vault_enabled,
    resolve_dotenv_file,
    use_vault_if_enabled,
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
        'vault': {
            'enabled': True,
            'path': 'root/path'
        },
        'stages': {
            'stage1': {
                'host': 'stage1.example.com',
                'remote_env_path': 'best',
                'vault': {
                    'path': 'root/path/stage1'
                }
            },
            'stage2': {
                'host': 'stage2.example.com',
                'port': '4321',
                'vault': {
                    'path': 'root/path/stage2'
                }
            },
            'stage3': {

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

    assert stage1_config['vault']['enabled'] is True
    assert stage1_config['vault']['path'] == 'root/path/stage1'

    # Stage 2
    stage2_config = result['stages']['stage2']
    assert stage2_config['port'] == raw_config['stages']['stage2']['port']
    assert stage2_config['host'] == raw_config['stages']['stage2']['host']
    assert stage2_config['remote_env_path'] == raw_config['remote_env_path']
    assert stage2_config['deployment'][
        'base_dir'] == raw_config['deployment']['base_dir']
    assert stage2_config['deployment'][
        'build_dir'] == DEFAULT_CONFIG['deployment']['build_dir']

    assert stage2_config['vault']['enabled'] is True
    assert stage2_config['vault']['path'] == 'root/path/stage2'

    # Stage 3
    stage3_config = result['stages']['stage3']
    assert stage3_config['vault']['enabled'] is True
    assert stage3_config['vault']['path'] == 'root/path'


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


@patch('boss.core.fs.read')
def test_load_with_env_vars(read_mock):
    '''
    Test load() function loads yaml file with env vars interpolation.
    '''
    read_mock.return_value = '''
    user: ${TEST_USER}
    project_name: ${TEST_PROJECT}
    port: 23
    deployment:
        preset: 'web'
        base_dir: ${TEST_BASE_DIR}
    '''
    os.environ['TEST_USER'] = 'test-user'
    os.environ['TEST_PROJECT'] = 'test-project'
    os.environ['TEST_BASE_DIR'] = '~/source/deployment'

    config_filename = 'test.yml'
    boss_config = load(config_filename)

    read_mock.assert_called_with(config_filename)

    # Configured options
    assert boss_config['user'] == 'test-user'
    assert boss_config['port'] == 23
    assert boss_config['project_name'] == 'test-project'
    assert boss_config['deployment']['preset'] == 'web'
    assert boss_config['deployment']['base_dir'] == '~/source/deployment'

    # Teardown
    os.environ['TEST_USER'] = ''
    os.environ['TEST_PROJECT'] = ''
    os.environ['TEST_BASE_DIR'] = ''


@patch('boss.core.fs.read')
@patch('boss.core.vault.read_secrets')
def test_load_with_env_vars_from_vault(read_secrets_mock, read_mock):
    '''
    Test load() function loads yaml file with
    env vars interpolation from vault.
    '''
    read_mock.return_value = '''
    user: ${TEST_USER}
    project_name: ${TEST_PROJECT}
    port: 24

    vault:
        enabled: true
        silent: true

    deployment:
        base_dir: ${TEST_BASE_DIR}

    test_var: $TEST_TEST_VAR

    stages:
        dev:
            test: test

        prod:
            user: $TEST_PROD_USER
    '''
    os.environ['TEST_USER'] = 'test-user-from-host'

    read_secrets_mock.return_value = {
        'TEST_PROJECT': 'test-project-from-vault',
        'TEST_BASE_DIR': 'test-base-dir-from-vault',
        'TEST_TEST_VAR': 'test-test-var-from-vault',
        'TEST_PROD_USER': 'test-prod-user-from-vault'
    }

    config_filename = 'test.yml'
    boss_config = load(config_filename)

    read_mock.assert_called_with(config_filename)
    read_secrets_mock.assert_called_with(DEFAULT_CONFIG['vault']['path'])

    # Configured options
    assert boss_config['user'] == 'test-user-from-host'
    assert boss_config['port'] == 24
    assert boss_config['project_name'] == 'test-project-from-vault'
    assert boss_config['deployment']['preset'] == 'remote-source'
    assert boss_config['deployment']['base_dir'] == 'test-base-dir-from-vault'

    # Stage specific
    assert boss_config['stages']['dev']['test'] == 'test'
    assert boss_config['stages']['dev']['user'] == 'test-user-from-host'
    assert boss_config['stages']['prod']['user'] == 'test-prod-user-from-vault'

    # Teardown
    os.environ['TEST_USER'] = ''
    os.environ['TEST_PROJECT'] = ''
    os.environ['TEST_BASE_DIR'] = ''
    os.environ['TEST_TEST_VAR'] = ''
    os.environ['TEST_PROD_USER'] = ''


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


def test_is_vault_enabled_returns_true():
    '''
    Test is_vault_enabled() returns True when it should.
    '''
    assert is_vault_enabled({'vault': {'enabled': True}}) is True


def test_is_vault_enabled_returns_false():
    '''
    Test is_vault_enabled() returns False when it should.
    '''
    assert is_vault_enabled({'vault': {'enabled': False}}) is False


def test_parse_config_returns_defaults_if_empty_config():
    ''' Test parse_config() returns defaults for empty config. '''
    result = parse_config('')

    assert result == DEFAULT_CONFIG


@patch('boss.core.vault.read_secrets')
def test_use_vault_if_enabled(read_secrets_mock):
    ''' Test use_vault_if_enabled() when vault enabled. '''
    config_str = '''
    user: ${TEST_USER}
    project_name: ${TEST_PROJECT}

    vault:
        enabled: true
        path: root/path
        silent: true
    '''

    os.environ['TEST_USER'] = 'test-user-from-host'

    read_secrets_mock.return_value = {
        'TEST_PROJECT': 'test-project-from-vault',
    }

    use_vault_if_enabled(config_str)

    read_secrets_mock.assert_called_with('root/path')
    # Configured options
    assert os.environ['TEST_USER'] == 'test-user-from-host'
    assert os.environ['TEST_PROJECT'] == 'test-project-from-vault'

    # Teardown
    os.environ['TEST_USER'] = ''
    os.environ['TEST_PROJECT'] = ''


@patch('boss.core.vault.read_secrets')
def test_use_vault_if_enabled_with_stage(read_secrets_mock):
    '''
    Test use_vault_if_enabled() when vault enabled
    with specific stage given.
    '''
    config_str = '''
    user: ${TEST_USER}
    project_name: ${TEST_PROJECT}

    vault:
        enabled: true
        path: root/path
        silent: true

    stages:
        stage1:
            vault:
                path: root/path/stage1
        stage2:
            test: test
    '''

    os.environ['TEST_USER'] = 'test-user-from-host'

    read_secrets_mock.return_value = {
        'TEST_PROJECT': 'test-project-from-vault',
    }

    # Test when invoked with stage=stage1
    # takes vault path for stage1
    use_vault_if_enabled(config_str, 'stage1')
    read_secrets_mock.assert_called_with('root/path/stage1')

    # Test when invoked with stage=stage2
    # takes the default vault path
    use_vault_if_enabled(config_str, 'stage2')
    read_secrets_mock.assert_called_with('root/path')

    # Env interpolation
    assert os.environ['TEST_USER'] == 'test-user-from-host'
    assert os.environ['TEST_PROJECT'] == 'test-project-from-vault'

    # Teardown
    os.environ['TEST_USER'] = ''
    os.environ['TEST_PROJECT'] = ''


@patch('boss.core.vault.read_secrets')
def test_use_vault_if_enabled_when_not_enabled(read_secrets_mock):
    '''
    Test use_vault_if_enabled() when vault is not enabled.
    It should just use the env vars from the host.
    '''
    config_str = '''
    user: ${TEST_USER}
    project_name: ${TEST_PROJECT}
    '''

    os.environ['TEST_USER'] = 'test-user-from-host'
    os.environ['TEST_PROJECT'] = ''

    read_secrets_mock.return_value = {
        'TEST_PROJECT': 'test-project-from-vault',
    }

    # Invoke with stage=stage1
    use_vault_if_enabled(config_str)
    read_secrets_mock.assert_not_called()

    # Env interpolation
    assert os.environ['TEST_USER'] == 'test-user-from-host'
    assert not os.environ['TEST_PROJECT']

    # Teardown
    os.environ['TEST_USER'] = ''
