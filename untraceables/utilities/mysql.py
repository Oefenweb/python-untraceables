# -*- coding: utf-8 -*-

"""
MySQL utility functions.
"""

from __future__ import absolute_import
from warnings import filterwarnings
import MySQLdb
import MySQLdb.cursors
from untraceables.utilities import query as query_utility

filterwarnings('ignore', category=MySQLdb.Warning)


def get_connection(host, user, password, database):
    """
    Gets a mysql connection to given database.

    :type str
    :param host: A host
    :type str
    :param user: A username
    :type str
    :param password: A password
    :type str
    :param database: A database name
    :rtype MySQLdb.connections.Connection
    :return A mysql connection
    """

    return MySQLdb.connect(host=host, user=user, passwd=password, db=database, cursorclass=MySQLdb.cursors.SSDictCursor)


def get_cursor(connection):
    """
    Gets a cursor from a given connection.

    :type MySQLdb.connections.Connection
    :param connection: A mysql connection
    :rtype MySQLdb.cursors.SSDictCursor
    :return A mysql cursor
    """

    return connection.cursor()


def close_connection_and_cursor(connection, cursor):
    """
    Closes a given connection and cursor.

    :type MySQLdb.connections.Connection
    :param connection: A mysql connection
    :type MySQLdb.cursors.SSDictCursor
    :param cursor: A mysql cursor
    :rtype bool
    :return: Success
    """

    attr = 'close'
    for to_be_closed_o in (cursor, connection):
        if hasattr(to_be_closed_o, attr):
            getattr(to_be_closed_o, attr)

    return True


def split_file(file_pointer, delimiter=';'):
    """
    Splits a SQL file by a given delimiter so it can be executed statement by statement.

    :type file
    :param file_pointer: The file pointer to an unsplitted SQL file
    :type str
    :param delimiter: A delimiter
    :rtype generator
    :return A splitted SQL file
    """

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
    """
    Gets the results of SHOW COLUMNS for a given table.

    :type MySQLdb.cursors.SSDictCursor
    :param cursor: A mysql cursor
    :type str
    :param table: A table name
    :rtype tuple
    :return The results of SHOW COLUMNS
    """

    return _fetchall(cursor, query_utility.get_show_table_columns(table))


def get_show_tables(cursor, database):
    """
    Gets the results of SHOW TABLES for a given database.

    :type MySQLdb.cursors.SSDictCursor
    :param cursor: A mysql cursor
    :type str
    :param database: A database name
    :rtype tuple
    :return The results of SHOW TABLES
    """

    return _fetchall(cursor, query_utility.get_show_columns(database))


def get_max_id(cursor, database, table, column, order=None):
    """
    Gets the maximum id for a given table / column.

    :type MySQLdb.cursors.SSDictCursor
    :param cursor: A mysql cursor
    :type str
    :param database: A database name
    :type str
    :param table: A table name
    :type str
    :param column: A column name
    :type str
    :param order: A column name to order on
    :rtype long|bool
    :return: The maximum id or False on failure
    """

    for row in _fetchall(cursor, query_utility.get_max_id(database, table, column, order)):
        return row[column]

    return False


def _fetchall(cursor, statement):
    """
    Fetches the results of a given SQL statement.

    :type MySQLdb.cursors.SSDictCursor
    :param cursor: A mysql cursor
    :type str
    :param statement: A SQL statement
    :rtype tuple
    :return The results of the MySQLdb statement
    """

    cursor.execute(statement)

    return cursor.fetchall()
