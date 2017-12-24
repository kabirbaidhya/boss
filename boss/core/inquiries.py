'''
A module to handle interaction of the CLI with the user.
'''
from inquirer import Text, List, prompt

from boss.core.constants import presets
from boss.core.constants.config import DEFAULT_CONFIG


def get_initial_config_params():
    ''' Get initial config params from user. '''

    questions = [
        Text(
            'project_name',
            message='Enter your project_name',
        ),

        Text(
            'user',
            message='Enter your SSH username',
            default=DEFAULT_CONFIG['user']
        ),

        Text(
            'ssh_port',
            message='Enter SSH port',
            default=DEFAULT_CONFIG['port']
        ),

        List(
            'deployment_preset',
            message='Select your deployment preset',
            choices=[
                presets.WEB,
                presets.NODE,
                presets.REMOTE_SOURCE
            ]
        ),

        Text(
            'deployment_base_dir',
            message='Enter your base directory for deployment',
            default=DEFAULT_CONFIG['deployment']['base_dir']
        )
    ]

    answers = prompt(questions)

    return answers
