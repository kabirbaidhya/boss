''' Notification constants. '''

from .notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED,
    RUNNING_SCRIPT_STARTED,
    RUNNING_SCRIPT_FINISHED
)

# TODO: Internationalization

MESSAGE_MAP = {
    DEPLOYMENT_STARTED: {
        'message': '{user} is deploying {project_link} to {server_link} server.',
        'message_with_branch': '{user} is deploying {project_link}:{branch_link} to {server_link} server.',
        'message_with_commit': '{user} is deploying {project_link} ({commit_link}) to {server_link} server.',
        'message_full': '{user} is deploying {project_link}:{branch_link} ({commit_link}) to {server_link} server.',
        # TODO: Rename this to started_color & ci_started_color
        'color': 'deploying_color',
        'ci_color': 'ci_deploying_color'
    },
    DEPLOYMENT_FINISHED: {
        'message': '{user} finished deploying {project_link} to {server_link} server.',
        'message_with_branch': '{user} finished deploying {project_link}:{branch_link} to {server_link} server.',
        'message_with_commit': '{user} finished deploying {project_link} ({commit_link}) to {server_link} server.',
        'message_full': '{user} finished deploying {project_link}:{branch_link} ({commit_link}) to {server_link} server.',
        # TODO: Rename this to started_color & ci_started_color
        'color': 'deployed_color',
        'ci_color': 'ci_deployed_color'
    },
    RUNNING_SCRIPT_STARTED: {
        'message': '{user} is running {project_link}:{script} on {server_link} server.',
        # TODO: Rename this to started_color & ci_started_color
        'color': 'deploying_color',
        'ci_color': 'ci_deploying_color'
    },
    RUNNING_SCRIPT_FINISHED: {
        'message': '{user} finished running {project_link}:{script} on {server_link} server.',
        # TODO: Rename this to started_color & ci_started_color
        'color': 'deployed_color',
        'ci_color': 'ci_deployed_color'
    }
}
