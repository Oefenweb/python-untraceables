# -*- coding: utf-8 -*-

"""
Cli utility functions.
"""

from __future__ import print_function

import sys


def config_unpack(config):
  """
  Unpacks relevant options from the configuration object.

  :type config: configobj.ConfigObj
  :param config: A configuration object
  :rtype tuple
  :return Relevant options
  """

  return config['main']['host'], config['main']['user'], config['main']['password']


def print_e(e):
  """
  Prints an error to `STDERR` and exits with a return code of `1`.

  :type e: mixed
  :param e: An error
  """

  print(e, file=sys.stderr)
  sys.exit(1)
