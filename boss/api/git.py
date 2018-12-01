from fabric.api import run, hide, local


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


def check_branch_exists(branch):
    ''' Check if a git branch exists on the remote. '''
    check = run('git rev-parse --verify ' + branch, quiet=True)

    return check.succeeded


def sync(ref):
    ''' Sync the current HEAD with the remote (origin)'s ref. '''
    # TODO: Custom origin
    branch_name = 'origin/' + ref

    if check_branch_exists(branch_name):
        run('git reset --hard ' + branch_name)
        return

    run('git reset --hard ' + ref)


def last_commit(remote=True, short=False):
    '''
    Get the last commit of the git repository.

    Note: This assumes the current working directory (on remote or local host)
    to be a git repository. So, make sure current directory is set before using this.
    '''

    cmd = 'git rev-parse{}HEAD'.format(' --short ' if short else ' ')

    with hide('everything'):
        result = run(cmd) if remote else local(cmd, capture=True)

        return result.strip()


def get_local_ref():
    ''' Get the current branch name or ref / commit if not available. '''
    branch = current_branch(remote=False)

    if branch != 'HEAD':
        return branch

    return last_commit(remote=False, short=True)


def current_branch(remote=True):
    '''
    Get the current branch of the git repository.

    Note: This assumes the current working directory (on remote or local host)
    to be a git repository. So, make sure current directory is set before using this.
    '''

    cmd = 'git rev-parse --abbrev-ref HEAD'

    with hide('everything'):
        result = run(cmd) if remote else local(cmd, capture=True)

        return result.strip()


def get_commit_url(commit, repository_url=None):
    ''' Get a link for a commit for GitHub. '''
    # TODO: Make it independent of GitHub.
    return '{repository_url}/commit/{commit}'.format(
        repository_url=repository_url,
        commit=commit
    ) if repository_url else None


def get_tree_url(ref, repository_url=None):
    ''' Get a link for a ref (commit, branch or tag) for the repository. '''
    return '{repository_url}/tree/{ref}'.format(
        repository_url=repository_url,
        ref=ref
    ) if repository_url else None


def show_last_commit():
    ''' Display the last commit. '''
    run('git log -1')
