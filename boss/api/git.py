from fabric.api import run


def fetch(prune=True):
    run('git fetch' + (' --prune' if prune else ''))


def checkout(branch):
    run('git checkout %s' % branch)


def pull(branch):
    run('git pull origin %s' % branch)
