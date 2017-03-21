# -*- coding: utf-8 -*-

import os

from configobj import ConfigObj


def read_file(filename):
  """
  Reads a configuration file and returns the configuration object (on success).

  Looks for the given configuration file in:
   * The current directory (.)
   * The users home directory (~)
   * Globally (/etc)

  @type filename: string
  @param filename: A (configuration) file name
  @rtype: mixed
  @return: A configuration object (dict) or False (boolean) on failure
  """

  for path in os.curdir, os.path.expanduser('~'), '/etc/':
    try:
      with open(os.path.join(path, filename)) as filepointer:
        config = ConfigObj(filepointer)

        return config
    except IOError:
      pass

  return False
