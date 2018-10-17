''' String Utilities. '''

import re

ANSI_CODES_REGEX = '\x1b[^m]*m'


def strip_ansi(text):
    ''' Strip ANSI escape character codes from a string. '''
    if not text:
        return text

    return re.sub(ANSI_CODES_REGEX, '', text)


def is_quoted(string):
    ''' Check if the provided string is quoted. '''
    return (
        len(string) > 0 and
        string[0] == string[-1] and
        string[0] in ['"', "'"]
    )
