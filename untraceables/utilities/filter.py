# -*- coding: utf-8 -*-

"""
Filter utility functions.
"""

import re


def _get_matches(input_columns, regexes):
  """
  Returns all of input columns where `table.column` matches a given set of regexes.

  :type input_columns: generator|set
  :param input_columns: Input columns
  :type regexes: list
  :param regexes: Zero or more regexes
  :rtype set
  :return Matches
  """

  patterns = [re.compile(r) for r in regexes]

  matched_columns = set()
  for input_column in input_columns:
    for pattern in patterns:
      if re.match(pattern, input_column):
        matched_columns.add(input_column)

  return matched_columns


def show_tables(table_columns, inclusive_regexes, exclusive_regexes):
  """
  Returns all columns that match a given set of inclusive regexes and don't match the exclusive regexes.

  Matching is done using `_get_matches`.

  :type table_columns: generator
  :param table_columns: Input columns (in format `table.column`)
  :type inclusive_regexes: list
  :param inclusive_regexes: Zero or more inclusive regexes
  :type exclusive_regexes: list
  :param exclusive_regexes: Zero or more exclusive regexes
  :rtype set
  :return Matches
  """

  included_columns = _get_matches(table_columns, inclusive_regexes)
  excluded_columns = _get_matches(included_columns, exclusive_regexes)

  return included_columns - excluded_columns

def table_names_from_mydumper_backup(files, suffixed_database):
  """

  :param files:
  :param suffixed_database:
  :return:
  """

  for file in files:
    if file.startswith(suffixed_database) and not file.endswith('schema.sql'):
      yield file
