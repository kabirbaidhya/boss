''' Notification constants. '''

from .notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED
)

MESSAGE_MAP = {
    DEPLOYMENT_STARTED: {
        'message': '{user} is deploying {project_link} ({commit_link}) to {server_link} server.',
        'message_with_branch': '{user} is deploying {project_link}:{branch_link} ({commit_link}) to {server_link} server.',
        'color': 'deploying_color',
        'ci_color': 'ci_deploying_color'
    },
    DEPLOYMENT_FINISHED: {
        'message': '{user} finished deploying {project_link} ({commit_link}) to {server_link} server.',
        'message_with_branch': '{user} finished deploying {project_link}:{branch_link} ({commit_link}) to {server_link} server.',
        'color': 'deployed_color',
        'ci_color': 'ci_deployed_color'
    }
}
