# -*- coding: utf-8 -*-

"""
Formatter utility functions.
"""

import os


def show_tables(table_columns):
  """
  Formats the results of SHOW TABLES.

   In the format `table.column`.

  :type tuple
  :param table_columns: Unformatted table columns
  :rtype generator
  :return Formatted table columns
  """

  for table_column in table_columns:
    yield '{0:s}.{1:s}'.format(table_column['TABLE_NAME'], table_column['COLUMN_NAME'])


def table_columns_tsv(database, table_columns):
  """
  Formats the results of SHOW COLUMNS.

   In the format `database<TAB>table<TAB>column`.

  :type str
  :param database: A database name
  :type list
  :param table_columns: Unformatted table columns
  :rtype generator
  :return Formatted table columns
  """

  for table_column in table_columns:
    table, column = table_column.split('.')
    yield '\t'.join((database, table, column))


def randomize_queries(queries):
  """
  Formats the results `query.get_randomize`

  :type list
  :param queries: Unformatted queries
  :rtype str
  :return Formatted queries
  """

  if len(queries) > 0:
    separator = ';' + os.linesep

    return separator.join(queries) + separator

  return ''


def table_names_from_mydumper_backup(files, suffixed_database):
  """

  :param files:
  :param suffixed_database:
  :return:
  """

  for file in files:
    yield os.path.splitext(file)[0].replace(suffixed_database, '')


def inclusive_regex_in(inclusive_regex, database_table_delimiter):
  """

  :param inclusive_regex:
  :param database_table_delimiter:
  :return:
  """

  splitted_regex = inclusive_regex.split(database_table_delimiter)
  table_regex = splitted_regex[0]
  field_regex = database_table_delimiter.join(splitted_regex[1:])

  return table_regex, field_regex


def inclusive_regex_out(file_basename, field_regex, database_table_delimiter):
  """

  :param file_basename:
  :param field_regex:
  :param database_table_delimiter:
  :return:
  """

  return database_table_delimiter.join(['^' + file_basename, field_regex])
