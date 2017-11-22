''' Core module for Continuous Integration (CI) operations. '''

from os import environ as env

from .constants import ci


def is_ci():
    ''' Check if boss is running in a Continuous Integration (CI) environment. '''

    return bool(
        env.get('BOSS_RUNNING') == 'true' and (
            (env.get('CI') == 'true') or
            (env.get('CONTINUOUS_INTEGRATION') == 'true')
        )
    )


def is_travis():
    ''' Check if boss is running under Travis CI. '''
    return is_ci() and env.get('TRAVIS') == 'true'


def get_ci_link(config):
    ''' Get CI build link for the current build deployment. '''
    if is_travis():
        base_url = config['ci']['base_url'].rstrip('/')

        return ci.TRAVIS_BUILD_URL.format(
            base_url=base_url,
            repo_slug=env.get('TRAVIS_REPO_SLUG'),
            build_id=env.get('TRAVIS_BUILD_ID')
        )

    # Other CI providers aren't supported at the moment.
    # TODO: Add support for more providers.

    return None
