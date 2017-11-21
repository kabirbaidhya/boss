''' Core module for Continuous Integration (CI) operations. '''

from os import environ as env


def is_ci():
    ''' Check if boss is running in a Continuous Integration (CI) environment. '''

    return bool(
        env.get('BOSS_RUNNING') == 'true' and (
            (env.get('CI') == 'true') or
            (env.get('CONTINUOUS_INTEGRATION') == 'true')
        )
    )
