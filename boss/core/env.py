''' Utility for parsing env declarations. '''

import codecs
from .util.string import is_quoted

__escape_decoder = codecs.getdecoder('unicode_escape')


def parse(env_def):
    ''' Parse env variable definitions. '''
    result = {}

    for line in env_def.splitlines():
        line = line.strip()

        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)

        # Remove any leading and trailing spaces in key, value
        key, value = key.strip(), value.strip().encode('unicode-escape').decode('ascii')

        if is_quoted(value):
            value = decode_escaped(value[1:-1])

        result[key] = value

    return result


def decode_escaped(escaped):
    return __escape_decoder(escaped)[0]
