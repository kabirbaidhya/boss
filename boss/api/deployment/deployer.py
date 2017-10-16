from boss import constants
from boss.util import halt


def import_preset(config):
    ''' Import the configured deployment preset module and return it. '''
    preset = config['deployment']['preset']

    if preset == constants.PRESET_REMOTE_SOURCE:
        from .preset import remote_source as module
    elif preset == constants.PRESET_WEB:
        from .preset import web as module
    elif preset == constants.PRESET_NODE:
        from .preset import node as module
    else:
        halt('Unsupported boss preset "{}".'.format(preset))

    return module
