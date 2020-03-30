# -*- coding: utf-8 -*-

"""
Cli utility functions.
"""

from __future__ import print_function
from __future__ import absolute_import
import sys

CONFIGURATION_FILE = 'untraceables.cfg'
"""
The name of untraceables' configuration file.

:type str
"""


def config_unpack(config):
    """
    Unpacks relevant options from the configuration object.

    :type config: configobj.ConfigObj
    :param config: A configuration object
    :rtype tuple
    :return Relevant options
    """

    return config['main']['host'], config['main']['user'], config['main']['password']


def print_e(error):
    """
    Prints an error to `STDERR` and exits with a return code of `1`.

    :type error: mixed
    :param error: An error
    """

    print(error, file=sys.stderr)
    sys.exit(1)
