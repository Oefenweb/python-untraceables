# -*- coding: utf-8 -*-

"""
Configuration utility functions.
"""

import os

from configobj import ConfigObj


def read_file(filename):
    """
    Reads a configuration file and returns the configuration object (on success).

     Looks for the given configuration file in:
      * The current directory (.)
      * The users home directory (~)
      * Globally (/etc)

    :type filename: str
    :param filename: A (configuration) file name
    :rtype bool|configobj.ConfigObj
    :return A configuration object or False on failure
    """

    for path in os.curdir, os.path.expanduser('~'), '/etc/':
        try:
            with open(os.path.join(path, filename)) as filepointer:
                return ConfigObj(filepointer)
        except IOError:
            pass

    return False


def read_xclude_regexes_file(filename):
    """
    Reads an ((in|ex)clude regexes) file and returns it's lines.

    :type filename: str
    :param filename: An ((in|ex)clude regexes) file name
    :rtype list
    :return File content lines
    """

    try:
        with open(filename) as filepointer:
            return filepointer.read().splitlines()
    except IOError:
        pass

    return []
