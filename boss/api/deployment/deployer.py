''' Deployer module. '''

from boss.core.output import halt
from boss.core.constants import presets


def import_preset(config):
    ''' Import the configured deployment preset module and return it. '''
    preset = config['deployment']['preset']

    if preset == presets.REMOTE_SOURCE:
        from .preset import remote_source as module
    elif preset == presets.WEB:
        from .preset import web as module
    elif preset == presets.NODE:
        from .preset import node as module
    else:
        halt('Unsupported boss preset "{}".'.format(preset))

    return module
