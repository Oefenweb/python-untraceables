# -*- coding: utf-8 -*-

"""
File utility functions.
"""

import os


def get_sorted_file_list(path):
  """
  Gets a sorted directory listing (files only) for a given path.

  :type path: string
  :param path: A path
  :rtype list
  :return Sorted file names
  """

  if os.path.exists(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return sorted(files)

  return []
