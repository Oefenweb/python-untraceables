# -*- coding: utf-8 -*-

from warnings import filterwarnings

import MySQLdb
import MySQLdb.cursors

from untraceables.utilities import query

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

  attr = 'close'
  for o in (cursor, connection):
    if hasattr(o, attr):
      getattr(o, attr)

  return True


def split_file(file_pointer, delimiter=';'):
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
  cursor.execute(query.get_show_table_columns(table))

  return cursor.fetchall()


def get_show_tables(cursor, database):
  cursor.execute(query.get_show_columns(database))

  return cursor.fetchall()
