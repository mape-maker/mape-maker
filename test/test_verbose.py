import logging
import sys
import verboselogs
from verbose import set_verbose_level

def test_lines():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical error message')

if __name__ == "__main__":
    logger = set_verbose_level()
    test_lines()