'''
Module to deal with the initialization of environment
for boss i.e generating config files and fabfile.
'''

from boss import BASE_PATH
from boss.core import fs
from boss.constants import DEFAULT_CONFIG, DEFAULT_CONFIG_FILE, FABFILE_PATH


def initialize():
    ''' Initialize the local project directory for boss. '''
    files_written = []
    fabfile = FABFILE_PATH
    config_file = DEFAULT_CONFIG_FILE

    # If config file doesn't exist create it.
    if not fs.exists(config_file):
        config_tmpl = fs.read(BASE_PATH + '/misc/boss.yml_template')
        config_tmpl = config_tmpl.format(
            project_name=DEFAULT_CONFIG['project_name'],
            user=DEFAULT_CONFIG['user'],
            deployment_preset=DEFAULT_CONFIG['deployment']['preset'],
            deployment_base_dir=DEFAULT_CONFIG['deployment']['base_dir']
        )
        fs.write(config_file, config_tmpl)
        files_written.append(config_file)

    # If fabfile doesn't exist create it.
    if not fs.exists(fabfile):
        fabfile_tmpl = fs.read(BASE_PATH + '/misc/fabfile.py_template')
        fs.write(fabfile, fabfile_tmpl)
        files_written.append(fabfile)

    return files_written
