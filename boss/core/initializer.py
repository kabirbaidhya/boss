'''
Module to deal with the initialization of environment
for boss i.e generating config files and fabfile.
'''

from boss import BASE_PATH
from boss.core import fs
from boss.constants import DEFAULT_CONFIG, DEFAULT_CONFIG_FILE, FABFILE_PATH

from boss.core.inquiries import get_initial_config_params


def initialize(interactive):
    ''' Initialize the local project directory for boss. '''
    files_written = []

    # Initialize fabfile first. If it already exists, a None is returned
    fabfile = initialize_fabfile()

    if fabfile:
        files_written.append(fabfile)

    # Initialize boss.yml next. If it already exists, a None is returned
    config_file = initialize_config(interactive)

    if config_file:
        files_written.append(config_file)

    return files_written


def initialize_config(interactive):
    '''
    Initialize a new boss.yml file.
    If the file already exists return None, else return the file.
    '''
    config_file = DEFAULT_CONFIG_FILE

    # If config already exists, return None
    if fs.exists(config_file):
        return None

    config_tmpl = fs.read(BASE_PATH + '/misc/boss.yml_template')

    if not interactive:
        tmpl_params = {
            'project_name': DEFAULT_CONFIG['project_name'],
            'user': DEFAULT_CONFIG['user'],
            'ssh_port': DEFAULT_CONFIG['port'],
            'deployment_preset': DEFAULT_CONFIG['deployment']['preset'],
            'deployment_base_dir': DEFAULT_CONFIG['deployment']['base_dir']
        }
    else:
        tmpl_params = get_initial_config_params()

    fs.write(config_file, config_tmpl.format(**tmpl_params))

    return config_file


def initialize_fabfile():
    '''
    Initialize a new fabfile.
    If the file already exists return None, else return the file.
    '''
    fabfile = FABFILE_PATH

    if not fs.exists(fabfile):
        fabfile_tmpl = fs.read(BASE_PATH + '/misc/fabfile.py_template')
        fs.write(fabfile, fabfile_tmpl)

        return fabfile
