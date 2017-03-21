# -*- coding: utf-8 -*-

from warnings import filterwarnings

import MySQLdb
import MySQLdb.cursors

filterwarnings('ignore', category=MySQLdb.Warning)


def get_connection(host, user, password, database):
  """
  Gets a mysql connection to given database.
  """

  return MySQLdb.connect(host=host, user=user, passwd=password, db=database, cursorclass=MySQLdb.cursors.SSDictCursor)


def get_cursor(connection):
  """
  Gets a cursor from a given connection.
  """

  return connection.cursor()


def close_connection_and_cursor(connection, cursor):
  """
  Closes a given connection and cursor.
  """

  cursor.close()
  connection.close()

  return True


def split_file(file_pointer, delimiter):
  buf = ''
  while True:
    while delimiter in buf:
      pos = buf.index(delimiter)
      yield buf[:pos]
      buf = buf[pos + len(delimiter):]
    chunk = file_pointer.read(4096)
    if not chunk:
      yield buf
      break
    buf += chunk


def get_show_columns(cursor, table):
  query = 'SHOW columns FROM `{:s}`'.format(table)
  cursor.execute(query)

  return cursor.fetchall()


def get_show_tables(cursor, database):
  query = ("SELECT"
           " CONCAT(`TABLE_NAME`, '.', `COLUMN_NAME`) AS `tc`"
           "FROM"
           " `information_schema`.`COLUMNS` "
           "WHERE"
           " `TABLE_SCHEMA` = '{:s}'").format(database)
  cursor.execute(query)

  for row in cursor.fetchall():
    yield row['tc']


def get_foreign_key_checks_query(value):
  yield 'SET FOREIGN_KEY_CHECKS={0:d}'.format(value)
