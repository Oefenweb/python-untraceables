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
        config = ConfigObj(filepointer)

        return config
    except IOError:
      pass

  return False
