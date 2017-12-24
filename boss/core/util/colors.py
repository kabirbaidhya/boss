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



# Color code constants
COLOR_GREY = '30'
COLOR_RED = '31'
COLOR_GREEN = '32'
COLOR_YELLOW = '33'
COLOR_BLUE = '34'
COLOR_MAGENTA = '35'
COLOR_CYAN = '36'
COLOR_WHITE = '37'


# Color util functions
grey = wrap_with_color(COLOR_GREY)
red = wrap_with_color(COLOR_RED)
green = wrap_with_color(COLOR_GREEN)
yellow = wrap_with_color(COLOR_YELLOW)
blue = wrap_with_color(COLOR_BLUE)
magenta = wrap_with_color(COLOR_MAGENTA)
cyan = wrap_with_color(COLOR_CYAN)
white = wrap_with_color(COLOR_WHITE)
