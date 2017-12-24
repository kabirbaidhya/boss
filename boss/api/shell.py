'''
Module that exposes functions related with the user's current execution shell.
'''

import sys
import commands

from boss.core.output import halt


def get_user():
    ''' Get the current user who is executing the script in the shell (Local). '''
    return commands.getoutput('whoami')


def get_stage():
    ''' Get the current stage name from the command line args. '''
    stage = sys.argv[1] if len(sys.argv) > 1 else None

    if stage is None:
        halt('No stage set for deployment')

    return stage
