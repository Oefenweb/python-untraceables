# -*- coding: utf-8 -*-

import os


def show_tables(table_columns):
  for table_column in table_columns:
    yield '{0:s}.{1:s}'.format(table_column['TABLE_NAME'], table_column['COLUMN_NAME'])


def table_columns_tsv(database, table_columns):
  for table_column in table_columns:
    table, column = table_column.split('.')
    yield '\t'.join((database, table, column))


def randomize_queries(queries):
  separator = ';' + os.linesep

  return separator.join(queries) + separator
