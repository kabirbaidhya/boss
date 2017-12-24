''' Console color utility functions. '''

import os


def wrap_with_color(code):
    '''
    Higher ordered function that returns a
    function to wrap text with color code.
    '''

    def inner(text, bold=False):
        c = code

        if os.environ.get('DISABLE_COLORS') or os.environ.get('FABRIC_DISABLE_COLORS'):
            return text

        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner


grey = wrap_with_color('30')
red = wrap_with_color('31')
green = wrap_with_color('32')
yellow = wrap_with_color('33')
blue = wrap_with_color('34')
magenta = wrap_with_color('35')
cyan = wrap_with_color('36')
white = wrap_with_color('37')
