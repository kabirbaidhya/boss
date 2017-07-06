from fabric.api import run, hide


def fetch(prune=True):
    ''' The git fetch command. '''
    run('git fetch' + (' --prune' if prune else ''))


def checkout(branch, force=False):
    ''' The git checkout command. '''
    force_flag = '-f ' if force else ''
    run('git checkout {0}{1}'.format(force_flag, branch))


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
