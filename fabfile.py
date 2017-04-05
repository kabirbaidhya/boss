from fabric.api import env, local

env.user = 'kabir'
env.hosts = ['localhost']


def test():
    local('npm --version')
