# -*- coding: utf-8 -*-

"""
File utility functions.
"""

import os


def get_sorted_file_list(path):
  """

  :param path:
  :return:
  """

  if os.path.exists(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return sorted(files)

  return []
