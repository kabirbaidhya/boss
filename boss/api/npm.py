from fabric.api import run as _run


def install():
    ''' The npm install command. '''
    _run('npm install')


def build():
    ''' The npm build command. '''
    _run('npm run build')


def test():
    ''' The npm test command. '''
    _run('npm test')


def prune():
    ''' The npm prune command. '''
    _run('npm prune')


def start():
    ''' The npm start command. '''
    _run('npm start')


def run(script):
    ''' Run an npm script defined in the package.json file. '''
    _run('npm run %s' % script)
