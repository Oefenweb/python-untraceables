# -*- coding: utf-8 -*-

import re


def _get_matches(input_columns, regexes):
  """
  Returns all elements of "input_columns" where "table.column" matches the regex.
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
  Returns all columns in database_columns that match the inclusive_regexes and don't match the exclusive_regexes.

  Matching is done using get_matches().
  """

  included_columns = _get_matches(table_columns, inclusive_regexes)
  excluded_columns = _get_matches(included_columns, exclusive_regexes)

  return included_columns - excluded_columns
