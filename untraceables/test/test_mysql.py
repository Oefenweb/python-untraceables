# -*- coding: utf-8 -*-

"""
Tests for `mysql_utility`.
"""

from __future__ import absolute_import
import os
import unittest
import MySQLdb
import MySQLdb.cursors

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
    """
    TestCase.
    """

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

        connection = ConnectionMock()
        cursor = None
        mysql_utility.close_connection_and_cursor(connection, cursor)
        self.assertRaisesRegex(Warning, 'close called on connection')

    def test_close_connection_and_cursor_close_called_on_cursor(self):
        """
        Tests `close_connection_and_cursor`.

        Cursor has a close method.
        """

        connection = None
        cursor = CursorMock()
        mysql_utility.close_connection_and_cursor(connection, cursor)
        self.assertRaisesRegex(Warning, 'close called on cursor')

    def test_split_file_0(self):
        """
        Tests `split_file`.

        One query per line.
        """
        file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test_split_file_0.sql')
        with open(file, 'r') as file_pointer:
            delimiter = ';'
            actual = mysql_utility.split_file(file_pointer)
            self.assertTrue(hasattr(actual, 'next') or hasattr(actual, '__next__'))
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

        actual = None
        try:
            actual = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
            self.assertIsInstance(actual, MySQLdb.connection)
        except Exception as e:
            raise e
        finally:
            mysql_utility.close_connection_and_cursor(actual, None)

    def test_get_connection_failure(self):
        """
        Tests `get_connection`.

        Failure.
        """

        try:
            mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, 'lorem', MYSQL_DATABASE)
        except Exception as e:
            self.assertIsInstance(e, MySQLdb.OperationalError)

    def test_get_cursor_success(self):
        """
        Tests `get_cursor`.

        Success.
        """

        connection = actual = None
        try:
            connection = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
            actual = mysql_utility.get_cursor(connection)
            self.assertIsInstance(actual, MySQLdb.cursors.SSDictCursor)
        except Exception as e:
            raise e
        finally:
            mysql_utility.close_connection_and_cursor(connection, actual)

    def test_get_cursor_failure(self):
        """
        Tests `get_cursor`.

        Failure.
        """

        try:
            mysql_utility.get_cursor(None)
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

    def test_get_show_columns(self):
        """
        Tests `get_show_columns`.
        """

        connection = actual = None
        try:
            connection = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
            cursor = mysql_utility.get_cursor(connection)
            table = 'users'
            actual = mysql_utility.get_show_columns(cursor, table)
            self.assertIsInstance(actual, tuple)
            self.assertEqual('id', actual[0]['Field'])
            self.assertEqual('mapped_id', actual[1]['Field'])
        except Exception as e:
            raise e
        finally:
            mysql_utility.close_connection_and_cursor(connection, cursor)

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

        connection = actual = None
        try:
            connection = mysql_utility.get_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
            cursor = mysql_utility.get_cursor(connection)
            expected = 2
            actual = mysql_utility.get_max_id(cursor, MYSQL_DATABASE, 'users', 'id')
            self.assertEqual(expected, actual)
            expected = 10
            actual = mysql_utility.get_max_id(cursor, MYSQL_DATABASE, 'users', 'mapped_id')
            self.assertEqual(expected, actual)
        except Exception as e:
            raise e
        finally:
            mysql_utility.close_connection_and_cursor(connection, cursor)


# pylint: disable=useless-object-inheritance,no-self-use,too-few-public-methods

class ConnectionMock(object):
    """
    Mock for connection.
    """

    def close(self):
        """
        To check that close is called.
        """
        raise Warning('close called on connection')


class CursorMock(object):
    """
    Mock for cursor.
    """

    def close(self):
        """
        To check that close is called.
        """
        raise Warning('close called on cursor')

# pylint: enable=useless-object-inheritance,no-self-use,too-few-public-methods

suite = unittest.TestLoader().loadTestsFromTestCase(TestMySql)
unittest.TextTestRunner(verbosity=2).run(suite)
