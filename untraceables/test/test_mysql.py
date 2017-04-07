# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors

import os
import unittest

from untraceables.utilities import mysql as mysql_utility

MYSQL_HOST = 'localhost'
"""
Tests database host.
"""

MYSQL_USER = 'untraceables'
"""
Tests database username.
"""

MYSQL_PASSWORD = 'mmRXHqnc3zSshYjxSv8n'
"""
Tests database password.
"""

MYSQL_DATABASE = 'untraceables_test'
"""
Tests database name.
"""


class TestMySql(unittest.TestCase):

  def test_close_connection_and_cursor_close_not_called(self):
    """
    Tests `close_connection_and_cursor`.

    Both connection and cursor have no method close.
    """

    connection = cursor = None
    actual = mysql_utility.close_connection_and_cursor(connection, cursor)
    self.assertTrue(actual)

  def test_close_connection_and_cursor_close_called_on_connection(self):
    """
    Tests `close_connection_and_cursor`.

    Connection has a close method.
    """

    connection = connection_mock()
    cursor = None
    actual = mysql_utility.close_connection_and_cursor(connection, cursor)
    self.assertRaisesRegexp(Warning, 'close called on connection')

  def test_close_connection_and_cursor_close_called_on_cursor(self):
    """
    Tests `close_connection_and_cursor`.

    Cursor has a close method.
    """

    connection = None
    cursor = cursor_mock()
    actual = mysql_utility.close_connection_and_cursor(connection, cursor)
    self.assertRaisesRegexp(Warning, 'close called on cursor')

  def test_split_file_0(self):
    """
    Tests `split_file`.

    One query per line.
    """
    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test_split_file_0.sql')
    with open(file, 'r') as file_pointer:
      delimiter = ';'
      actual = mysql_utility.split_file(file_pointer)
      self.assertTrue(hasattr(actual, 'next'))
      actual_as_list = list(actual)
      expected = 'SELECT NOW()'
      self.assertEqual(expected, actual_as_list[0])
      expected = '\nSELECT 1'
      self.assertEqual(expected, actual_as_list[1])
      expected = '\n'
      self.assertEqual(expected, actual_as_list[3])

    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test_split_file_0.sql')
    with open(file, 'r') as file_pointer:
      delimiter = ';'
      actual = mysql_utility.split_file(file_pointer, delimiter)
      actual_as_list = list(actual)
      expected = 'SELECT NOW()'
      self.assertEqual(expected, actual_as_list[0])
      expected = '\nSELECT 1'
      self.assertEqual(expected, actual_as_list[1])
      expected = '\n'
      self.assertEqual(expected, actual_as_list[3])

  def test_split_file_1(self):
    """
    Tests `split_file`.

    All queries on one line.
    """

    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test_split_file_1.sql')
    with open(file, 'r') as file_pointer:
      delimiter = ';'
      actual = mysql_utility.split_file(file_pointer, delimiter)
      actual_as_list = list(actual)
      expected = 'SELECT NOW()'
      self.assertEqual(expected, actual_as_list[0])
      expected = ' SELECT 1'
      self.assertEqual(expected, actual_as_list[1])
      expected = '\n'
      self.assertEqual(expected, actual_as_list[3])

  def test_split_file_2(self):
    """
    Tests `split_file`.


    All queries on one line, $ as delimiter.
    """

    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test_split_file_2.sql')
    with open(file, 'r') as file_pointer:
      delimiter = '$'
      actual = mysql_utility.split_file(file_pointer, delimiter)
      actual_as_list = list(actual)
      expected = 'SELECT NOW()'
      self.assertEqual(expected, actual_as_list[0])
      expected = ' SELECT 1'
      self.assertEqual(expected, actual_as_list[1])
      expected = '\n'
      self.assertEqual(expected, actual_as_list[3])

  def test_get_connection_success(self):
    """
    Tests `get_connection`.

    Success.
    """

    actual = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    self.assertIsInstance(actual, MySQLdb.connection)

  def test_get_connection_failure(self):
    """
    Tests `get_connection`.

    Failure.
    """

    try:
      actual = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, 'lorem', MYSQL_DATABASE)
    except Exception, e:
      self.assertIsInstance(e, MySQLdb.OperationalError)

  def test_get_cursor_success(self):
    """
    Tests `get_cursor`.

    Success.
    """

    connection = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    actual = mysql_utility.get_cursor(connection)
    self.assertIsInstance(actual, MySQLdb.cursors.SSDictCursor)

  def test_get_cursor_failure(self):
    """
    Tests `get_cursor`.

    Failure.
    """

    try:
      actual = mysql_utility.get_cursor(None)
    except Exception, e:
      self.assertIsInstance(e, AttributeError)

  def test_get_show_columns(self):
    """
    Tests `get_show_columns`.
    """

    cursor = mysql_utility.get_cursor(mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD,
                                                                   MYSQL_DATABASE))
    table = 'users'
    actual = mysql_utility.get_show_columns(cursor, table)
    self.assertIsInstance(actual, tuple)
    self.assertEqual('id', actual[0]['Field'])
    self.assertEqual('mapped_id', actual[1]['Field'])

  def test_get_show_tables(self):
    """
    Tests `get_show_tables`.
    """

    connection = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    cursor = mysql_utility.get_cursor(connection)
    actual = mysql_utility.get_show_tables(cursor, MYSQL_DATABASE)
    self.assertIsInstance(actual, tuple)
    self.assertEqual({'TABLE_NAME': 'users', 'COLUMN_NAME': 'id'}, actual[0])
    self.assertEqual({'TABLE_NAME': 'users', 'COLUMN_NAME': 'mapped_id'}, actual[1])

  def test_get_max_id(self):
    """
    Tests `get_max_id`.
    """

    connection = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    cursor = mysql_utility.get_cursor(connection)
    expected = 2
    actual = mysql_utility.get_max_id(cursor, MYSQL_DATABASE, 'users', 'id')
    self.assertEqual(expected, actual)
    expected = 10
    actual = mysql_utility.get_max_id(cursor, MYSQL_DATABASE, 'users', 'mapped_id')
    self.assertEqual(expected, actual)


class connection_mock(object):
  def close(self):
    raise Warning('close called on connection')


class cursor_mock(object):
  def close(self):
    raise Warning('close called on cursor')

suite = unittest.TestLoader().loadTestsFromTestCase(TestMySql)
unittest.TextTestRunner(verbosity=2).run(suite)
