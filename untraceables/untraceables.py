# -*- coding: utf-8 -*-

import re
import os


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


def filter_table_list(table_columns, inclusive_regexes, exclusive_regexes):
  """
  Returns all columns in database_columns that match the inclusive_regexes and don't match the exclusive_regexes.

  Matching is done using get_matches().
  """

  included_columns = _get_matches(table_columns, inclusive_regexes)
  excluded_columns = _get_matches(included_columns, exclusive_regexes)

  return included_columns - excluded_columns


def format_table_list(database, table_columns):
  for table_column in table_columns:
    table, column = table_column.split('.')
    yield '\t'.join((database, table, column))


def get_randomize_queries(database, table, columns, column, mapping_database, mapping_table):
  queries = []
  queries.append('DROP TABLE IF EXISTS `{:s}`.`_{:s}`'.format(database, table))
  queries.append('CREATE TABLE `{0:s}`.`_{1:s}` LIKE `{0:s}`.`{1:s}`'.format(database, table))
  queries.append(_get_randomize_query(database, table, columns, column, mapping_database, mapping_table))
  queries.append('DROP TABLE `{:s}`.`{:s}`'.format(database, table))
  queries.append('RENAME TABLE `{0:s}`.`_{1:s}` TO `{0:s}`.`{1:s}`'.format(database, table))

  return queries


def _get_randomize_query(database, table, columns, column, mapping_database, mapping_table):
  query = []
  query.append('INSERT INTO `{:s}`.`_{:s}`'.format(database, table))
  query.append('SELECT')

  select = []
  for c in columns:
    if c['Field'] == column:
      select.append('`t2`.`mapped_id`')
    else:
      select.append('`t1`.`{:s}`'.format(c['Field']))
  query.append(', '.join(select))

  query.append('FROM `{:s}`.`{:s}` `t1`'.format(database, table))
  query.append('LEFT JOIN `{:s}`.`{:s}` `t2` ON `t2`.`id` = `t1`.`{:s}`'.format(mapping_database,
                                                                                mapping_table,
                                                                                column))

  return ' '.join(query)


def format_randomize_queries(queries):
  separator = ';' + os.linesep

  return separator.join(queries) + separator
