"""
Supported options:
  -v, --verbose_level
  SPAM: level >= 4
  DEBUG: level >= 3
  VERBOSE: level >= 2
  NOTICE: level >= 1
  WARNING: level <= 0
"""

import logging, verboselogs
import sys

def set_verbose_level(level = 10):
    logger = verboselogs.VerboseLogger('verbose-demo')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    # Command line option defaults.
    verbosity = 0
    # Parse command line options.
    if not isinstance(level, int):
        print(level, " should be integer")
        print (__doc__.strip())
        sys.exit(0)
    else:
        verbosity = level
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
    logger = set_verbose_level(10)
    print(logger.level)