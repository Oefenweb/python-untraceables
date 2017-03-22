# -*- coding: utf-8 -*-

"""
Query utility functions.
"""

import untraceables


def get_show_table_columns(table):
  """
  Gets the query of SHOW COLUMNS for a given table.

  :type str
  :param table: A table name
  :rtype str
  :return A query
  """

  return 'SHOW COLUMNS FROM `{:s}`'.format(table)


def get_show_columns(database):
  """
  Gets the query of SHOW COLUMNS for a given database.

  :type str
  :param database: A database name
  :rtype str
  :return A query
  """

  return ("SELECT `TABLE_NAME`, `COLUMN_NAME` "
          " FROM "
          "`information_schema`.`COLUMNS`"
          " WHERE "
          "`TABLE_SCHEMA` = '{:s}'").format(database)


def get_max_id(database, table, column, order=None):
  """
  Gets the query to determine the maximum id for a given table / column.

  :type str
  :param database: A database name
  :type str
  :param table: A table name
  :type str
  :param column: A column name
  :type str
  :param order: A column name to order on
  :rtype long
  :return The maximum id
  """

  if not order:
    order = column

  return 'SELECT `{:s}` FROM `{:s}`.`{:s}` ORDER BY `{:s}` DESC LIMIT 1'.format(column, database, table, order)


def get_foreign_key_checks(enabled):
  """
  Gets the query the enable / disable FOREIGN_KEY_CHECKS.

  :type bool
  :param enabled: Whether or not to enable
  :rtype str
  :return A query
  """

  return 'SET FOREIGN_KEY_CHECKS={0:d}'.format(enabled)


def get_randomize(database, table, columns, column, mapping_database, mapping_table):
  """
  Gets the queries to randomize a table / column in a given database.

  :type str
  :param database: A database name
  :type str
  :param table: A table name
  :type str
  :param columns: A column name
  :type tuple
  :param column: Zero or more columns
  :type str
  :param mapping_database: A mapping database name (e.g. `untraceables`)
  :type str
  :param mapping_table: A mapping table name (e.g. `users`)
  :rtype list
  :return Multiple queries
  """

  queries = []
  queries.append('DROP TABLE IF EXISTS `{:s}`.`_{:s}`'.format(database, table))
  queries.append('CREATE TABLE `{0:s}`.`_{1:s}` LIKE `{0:s}`.`{1:s}`'.format(database, table))
  queries.append(_get_randomize(database, table, columns, column, mapping_database, mapping_table))
  queries.append('DROP TABLE `{:s}`.`{:s}`'.format(database, table))
  queries.append('RENAME TABLE `{0:s}`.`_{1:s}` TO `{0:s}`.`{1:s}`'.format(database, table))

  return queries


def _get_randomize(database, table, columns, column, mapping_database, mapping_table):
  """
  Gets the query to randomize a table / column in a given database.

   INSERT INTO ... SELECT FROM ... part.

  :type str
  :param database: A database name
  :type str
  :param table: A table name
  :type str
  :param columns: A column name
  :type tuple
  :param column: Zero or more columns
  :type str
  :param mapping_database: A mapping database name (e.g. `untraceables`)
  :type str
  :param mapping_table: A mapping table name (e.g. `users`)
  :rtype str
  :return A query
  """

  query = []
  query.append('INSERT INTO `{:s}`.`_{:s}`'.format(database, table))
  query.append('SELECT')

  select = []
  for c in columns:
    if c['Field'] == column:
      select.append('`t2`.`{:s}`'.format(untraceables.MAPPING_ID_FIELD))
    else:
      select.append('`t1`.`{:s}`'.format(c['Field']))
  query.append(', '.join(select))

  query.append('FROM `{:s}`.`{:s}` `t1`'.format(database, table))
  query.append('LEFT JOIN `{:s}`.`{:s}` `t2` ON `t2`.`id` = `t1`.`{:s}`'.format(mapping_database,
                                                                                mapping_table,
                                                                                column))

  return ' '.join(query)
