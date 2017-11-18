''' String Utilities. '''

import re

ANSI_CODES_REGEX = '\x1b[^m]*m'


def strip_ansi(text):
    ''' Strip ANSI escape character codes from a string. '''
    return re.sub(ANSI_CODES_REGEX, '', text)
