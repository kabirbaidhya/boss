''' Utility for parsing env declarations. '''

import codecs

__escape_decoder = codecs.getdecoder('unicode_escape')


def parse(env_def):
    ''' Parse env variable definations. '''
    result = {}

    for line in env_def.splitlines():
        line = line.strip()

        if not line or line.startswith('#') or '=' not in line:
            continue

        k, v = line.split('=', 1)

        # Remove any leading and trailing spaces in key, value
        k, v = k.strip(), v.strip().encode('unicode-escape').decode('ascii')

        if len(v) > 0:
            quoted = v[0] == v[len(v) - 1] in ['"', "'"]

            if quoted:
                v = decode_escaped(v[1:-1])

        result[k] = v

    return result


def decode_escaped(escaped):
    return __escape_decoder(escaped)[0]
