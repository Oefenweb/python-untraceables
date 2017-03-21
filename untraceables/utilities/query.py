# -*- coding: utf-8 -*-

def get_show_table_columns(table):
  return 'SHOW columns FROM `{:s}`'.format(table)


def get_show_columns(database):
 return ("SELECT `TABLE_NAME`, `COLUMN_NAME` "
         " FROM "
         "`information_schema`.`COLUMNS`"
         " WHERE "
         "`TABLE_SCHEMA` = '{:s}'").format(database)


def get_foreign_key_checks(enabled):
  return 'SET FOREIGN_KEY_CHECKS={0:d}'.format(enabled)


def get_randomize(database, table, columns, column, mapping_database, mapping_table):
  queries = []
  queries.append('DROP TABLE IF EXISTS `{:s}`.`_{:s}`'.format(database, table))
  queries.append('CREATE TABLE `{0:s}`.`_{1:s}` LIKE `{0:s}`.`{1:s}`'.format(database, table))
  queries.append(_get_randomize(database, table, columns, column, mapping_database, mapping_table))
  queries.append('DROP TABLE `{:s}`.`{:s}`'.format(database, table))
  queries.append('RENAME TABLE `{0:s}`.`_{1:s}` TO `{0:s}`.`{1:s}`'.format(database, table))

  return queries


def _get_randomize(database, table, columns, column, mapping_database, mapping_table):
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
