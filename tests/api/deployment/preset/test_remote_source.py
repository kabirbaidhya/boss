''' Tests for boss.api.deployment.preset.remote_source. '''

from mock import patch
from boss.api.deployment.preset import remote_source


@patch('boss.api.deployment.preset.remote_source.get_stage_config')
@patch('boss.api.git.get_local_ref')
def test_resolve_deployment_branch(m_cb, m_gsc):
    '''
    Test resolve_deployment_branch()
    when branch if use_local_ref = True.
    '''
    m_cb.return_value = 'the-local-ref'
    m_gsc.return_value = {
        'deployment': {
            'use_local_ref': True
        }
    }
    result = remote_source.resolve_deployment_branch('my_stage')

    assert result == 'the-local-ref'


@patch('boss.api.deployment.preset.remote_source.get_stage_config')
def test_resolve_deployment_branch_returns_default_branch(m_gsc):
    '''
    Test resolve_deployment_branch() returns stage default
    when branch if use_local_ref = False.
    '''
    m_gsc.return_value = {
        'deployment': {
            'use_local_ref': False
        },
        'branch': 'default-branch'
    }
    result = remote_source.resolve_deployment_branch('my_stage')

    assert result == 'default-branch'
