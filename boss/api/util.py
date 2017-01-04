import commands
import boss
from fabric.api import run, hide


def get_user():
    return commands.getoutput('whoami')


def get_branch_url(branch):
    return boss.config['repository_url'] + '/branch/' + branch


def get_remote_branch():
    with hide('everything'):
        result = run('git rev-parse --abbrev-ref HEAD')

    return result.strip()
