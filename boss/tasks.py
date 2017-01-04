from boss.util import info
from boss.api import git, bower, npm, systemctl


def git_fetch(prune=True):
    info('Fetching the latest changes')
    git.fetch(prune)


def git_checkout(branch):
    info('Checking out to the %s branch' % branch)
    git.checkout(branch)


def git_pull(branch):
    info('Pulling the latest changes of the %s branch' % branch)
    git.pull(branch)


def pull(branch=None):
    branch = branch or git.get_remote_branch()
    git_pull(branch)


def sync(branch=None):
    git_fetch()
    branch = branch or git.get_remote_branch()
    git_checkout(branch)
    git.sync_origin(branch)


def bower_install():
    info('Bower: Installing dependencies')
    bower.install()


def npm_install():
    info('Npm: Installing dependencies')
    npm.install()


def systemctl_enable(service=None):
    systemctl.enable(service)


def systemctl_restart(service=None):
    systemctl.restart(service)


def systemctl_status(service=None):
    systemctl.status(service)
