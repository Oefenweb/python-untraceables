# -*- coding: utf-8 -*-

import unittest

from untraceables.utilities import query


class TestQuery(unittest.TestCase):

  def test_get_show_table_columns(self):
    """
    Tests `get_show_table_columns`.
    """

    table = 'lorem'
    actual = query.get_show_table_columns(table)
    expected = 'SHOW COLUMNS FROM `lorem`'
    self.assertEqual(expected, actual)

  def test_get_show_columns(self):
    """
    Tests `get_show_columns`.
    """

    database = 'lorem'
    actual = query.get_show_columns(database)
    expected = 'SELECT `TABLE_NAME`, `COLUMN_NAME`'
    self.assertTrue(expected in actual)
    expected = 'WHERE `TABLE_SCHEMA` = \'lorem\''
    self.assertTrue(expected in actual)

  def test_get_max_id(self):
    """
    Tests `get_max_id`.
    """

    database = 'lorem'
    table = 'ipsum'
    column = 'dolor'
    order = 'sit'

    actual = query.get_max_id(database, table, column)
    expected = 'SELECT `dolor` FROM `lorem`.`ipsum` ORDER BY `dolor` DESC LIMIT 1'
    self.assertEqual(expected, actual)
    actual = query.get_max_id(database, table, column, order)
    expected = 'SELECT `dolor` FROM `lorem`.`ipsum` ORDER BY `sit` DESC LIMIT 1'
    self.assertEqual(expected, actual)

  def test_get_foreign_key_checks(self):
    """
    Tests `get_foreign_key_checks`.
    """

    actual = query.get_foreign_key_checks(True)
    expected = 'SET FOREIGN_KEY_CHECKS=1'
    self.assertEqual(expected, actual)
    actual = query.get_foreign_key_checks(1)
    self.assertEqual(expected, actual)

    actual = query.get_foreign_key_checks(False)
    expected = 'SET FOREIGN_KEY_CHECKS=0'
    self.assertEqual(expected, actual)
    actual = query.get_foreign_key_checks(0)
    self.assertEqual(expected, actual)

  def test_get_randomize(self):
    """
    Tests `get_randomize`.
    """

    database = 'lorem'
    table = 'ipsum'
    columns = ({'Field': 'dolor'}, {'Field': 'sit'}, {'Field': 'amet'})
    column = 'consectetur'
    mapping_database = 'adipiscing'
    mapping_table = 'elit'

    expected = type(list())
    actual = query.get_randomize(database, table, columns, column, mapping_database, mapping_table)
    self.assertEqual(expected, type(actual))
    self.assertTrue(len(actual) > 0)

    expected = 'DROP TABLE IF EXISTS `lorem`.`_ipsum`'
    self.assertEqual(expected, actual[0])
    expected = 'CREATE TABLE `lorem`.`_ipsum` LIKE `lorem`.`ipsum`'
    self.assertEqual(expected, actual[1])
    expected = ('INSERT INTO `lorem`.`_ipsum` '
                'SELECT `t1`.`dolor`, `t1`.`sit`, `t1`.`amet` '
                'FROM `lorem`.`ipsum` `t1` '
                'LEFT JOIN `adipiscing`.`elit` `t2` ON `t2`.`id` = `t1`.`consectetur`')
    self.assertEqual(expected, actual[2])
    expected = 'DROP TABLE `lorem`.`ipsum`'
    self.assertEqual(expected, actual[3])
    expected = 'RENAME TABLE `lorem`.`_ipsum` TO `lorem`.`ipsum`'
    self.assertEqual(expected, actual[4])

suite = unittest.TestLoader().loadTestsFromTestCase(TestQuery)
unittest.TextTestRunner(verbosity=2).run(suite)
