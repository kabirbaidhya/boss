import os
import mockssh
import tempfile
from pytest import yield_fixture

from boss import BASE_PATH
SAMPLE_USER_KEY = os.path.join(BASE_PATH, 'misc/sample-keys/user-key')


@yield_fixture(scope='function')
def server():
    ''' Mock SSH Server. '''
    users = {'sample-user': SAMPLE_USER_KEY}
    with mockssh.Server(users) as s:
        s.ROOT_DIR = tempfile.mkdtemp()
        yield s
