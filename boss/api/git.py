from fabric.api import run, hide


def fetch(prune=True):
    ''' The git fetch command. '''
    run('git fetch' + (' --prune' if prune else ''))


def checkout(branch):
    ''' The git checkout command. '''
    run('git checkout %s' % branch)


def pull(branch):
    ''' The git pull command. '''
    run('git pull origin %s' % branch)
    # TODO: Custom origin


def remote_branch():
    ''' Get the current branch of the remote server. '''
    with hide('everything'):
        result = run('git rev-parse --abbrev-ref HEAD')

    return result.strip()


def sync(branch):
    ''' Sync the current HEAD with the remote(origin)'s branch '''
    run('git reset --hard origin/%s' % branch)
    # TODO: Custom origin


def show_last_commit():
    ''' Display the last commit. '''
    run('git log -1')
