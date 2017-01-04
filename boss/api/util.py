import commands
import boss


def get_user():
    return commands.getoutput('whoami')


def get_branch_url(branch):
    return boss.config['repository_url'] + '/branch/' + branch
