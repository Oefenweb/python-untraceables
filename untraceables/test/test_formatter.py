# -*- coding: utf-8 -*-

import unittest

from untraceables.utilities import formatter


class TestFormatter(unittest.TestCase):

  def test_show_tables(self):
    """
    Tests `show_tables`.
    """

    table_columns = ()
    expected = iter([])
    actual = formatter.show_tables(table_columns)
    self.assertTrue(hasattr(actual, 'next'))
    self.assertEquals(list(expected), list(actual))

    table_columns = ({'TABLE_NAME': 'lorem', 'COLUMN_NAME': 'ipsum'},)
    expected = iter(['lorem.ipsum'])
    actual = formatter.show_tables(table_columns)
    self.assertEquals(list(expected), list(actual))

    table_columns = ({'TABLE_NAME': 'lorem', 'COLUMN_NAME': 'ipsum'}, {'TABLE_NAME': 'dolor', 'COLUMN_NAME': 'sit'})
    expected = iter(['lorem.ipsum', 'dolor.sit'])
    actual = formatter.show_tables(table_columns)
    self.assertEquals(list(expected), list(actual))

  def test_table_columns_tsv(self):
    """
    Tests `table_columns_tsv`.
    """

    database = 'adipiscing'
    table_columns = ['lorem.ipsum', 'dolor.sit']
    expected = ['adipiscing\tlorem\tipsum', 'adipiscing\tdolor\tsit']
    actual = formatter.table_columns_tsv(database, table_columns)
    self.assertEquals(list(expected), list(actual))

  def test_randomize_queries(self):
    """
    Tests `randomize_queries`.
    """

    queries = ['SELECT NOW()', 'SELECT 1']
    expected = ('SELECT NOW();\n'
                'SELECT 1;\n')
    actual = formatter.randomize_queries(queries)
    self.assertEquals(expected, actual)

    queries = []
    expected = ''
    actual = formatter.randomize_queries(queries)
    self.assertEquals(expected, actual)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFormatter)
unittest.TextTestRunner(verbosity=2).run(suite)
