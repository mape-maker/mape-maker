"""
Supported options:
  -v, --verbose  make more noise
  -h, --help     show this message and exit
"""

import getopt
import logging
import sys
import verboselogs

logger = verboselogs.VerboseLogger('demo')
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG)
# Command line option defaults.
verbosity = 0
# Parse command line options.
opts, args = getopt.getopt(sys.argv[1:], 'v:q:', ['-verbose=', '-quiet='])
print(opts, args)
# Map command line options to variables.
for option, argument in opts:
    if option in ('-v', '--verbose'):
        verbosity += int(argument)
    elif option in ('-q', '--quiet'):
        verbosity -= int(argument)
    else:
        assert False, "Unhandled option!"


# Configure logger for requested verbosity.
if verbosity >= 4:
    # The value of SPAM positions the spam log level
    # between the DEBUG and NOTSET levels.
    logger.setLevel(logging.SPAM)
elif verbosity >= 3:
    # Detailed information, typically of interest
    # only when diagnosing problems.
    logger.setLevel(logging.DEBUG)
elif verbosity >= 2:
    # The value of VERBOSE positions the verbose log level
    # between the INFO and DEBUG levels.
    logger.setLevel(logging.VERBOSE)
elif verbosity >= 1:
    # The value of NOTICE positions the notice log level
    # between the WARNING and INFO levels.
    logger.setLevel(logging.NOTICE)
elif verbosity < 0:
    # An indication that something unexpected happened.
    logger.setLevel(logging.WARNING)

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything