"""
Supported options:
  -v, -verbose=  make more noise
  -q, -quiet=  decrease the noise
  -h, --help
"""

import logging, verboselogs
import sys
import getopt

def set_verbose_level():
    logger = verboselogs.VerboseLogger('verbose-demo')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    # Command line option defaults.
    verbosity = 0
    # Parse command line options.
    opts, args = getopt.getopt(sys.argv[1:], 'v:q:h', ['-verbose=', '-quiet=', '-help'])
    print(opts, args)
    # Map command line options to variables.
    for option, argument in opts:
        if option in ('-v', '--verbose'):
            verbosity += int(argument)
        elif option in ('-q', '--quiet'):
            verbosity -= int(argument)
        elif option in ('-h', '--help'):
            print (__doc__.strip())
            sys.exit(0)
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
    elif verbosity <= 0:
        # An indication that something unexpected happened.
        print("done")
        logger.setLevel(logging.WARNING)
    return logger

# to run it from console like a simple script use
if __name__ == "__main__":

    logger = set_verbose_level()
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical error message')
