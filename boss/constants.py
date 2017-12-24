''' Application wide common constants module. '''

from os.path import expanduser

# Default boss configuration
DEFAULT_CONFIG_FILE = 'boss.yml'
FABFILE_PATH = 'fabfile.py'

# Boss paths
BOSS_HOME_PATH = expanduser('~/.boss')
BOSS_CACHE_PATH = BOSS_HOME_PATH + '/cache'
