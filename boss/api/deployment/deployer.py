from boss import constants
from boss.util import warn_deprecated, halt


def import_preset(config):
    ''' Import the configured deployment preset module and return it. '''
    preset = config['deployment']['preset']

    if not preset:
        warn_deprecated(
            'Set deployment preset explicitly, if you need deployment tasks. ' +
            'In the future releases, deployment tasks won\'t be available unless ' +
            'you have set the preset.'
        )
        # TODO: In future release, don't import deployment tasks
        # unless the preset is set. (BC Break)
        from .preset import remote_source as module
    elif preset == constants.PRESET_REMOTE_SOURCE:
        from .preset import remote_source as module
    elif preset == constants.PRESET_FRONTEND:
        from .preset import frontend as module
    else:
        halt('Unsupported boss preset "{}".'.format(preset))

    return module
