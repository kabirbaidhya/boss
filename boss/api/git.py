from fabric.api import run, hide


def fetch(prune=True):
    run('git fetch' + (' --prune' if prune else ''))


def checkout(branch):
    run('git checkout %s' % branch)


def pull(branch):
    run('git pull origin %s' % branch)


def get_remote_branch():
    with hide('everything'):
        result = run('git rev-parse --abbrev-ref HEAD')

    return result.strip()


def sync_origin(branch):
    run('git reset --hard origin/%s' % branch)
