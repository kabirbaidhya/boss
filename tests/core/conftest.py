import os
from pytest import yield_fixture
import mockssh

from boss import BASE_PATH

SAMPLE_USER_KEY = os.path.join(BASE_PATH, 'misc/sample-keys/user-key')


@yield_fixture(scope='function')
def server():
    ''' Mock SSH Server. '''
    users = {'sample-user': SAMPLE_USER_KEY}
    with mockssh.Server(users) as s:
        yield s
