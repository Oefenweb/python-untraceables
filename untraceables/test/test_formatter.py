# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest
from untraceables.utilities import formatter as formatter_utility


class TestFormatter(unittest.TestCase):

    def test_show_tables(self):
        """
        Tests `show_tables`.
        """

        table_columns = ()
        expected = iter([])
        actual = formatter_utility.show_tables(table_columns)
        self.assertTrue(hasattr(actual, 'next') or hasattr(actual, '__next__'))
        self.assertEquals(list(expected), list(actual))

        table_columns = ({'TABLE_NAME': 'lorem', 'COLUMN_NAME': 'ipsum'},)
        expected = iter(['lorem.ipsum'])
        actual = formatter_utility.show_tables(table_columns)
        self.assertEquals(list(expected), list(actual))

        table_columns = ({'TABLE_NAME': 'lorem', 'COLUMN_NAME': 'ipsum'}, {'TABLE_NAME': 'dolor', 'COLUMN_NAME': 'sit'})
        expected = iter(['lorem.ipsum', 'dolor.sit'])
        actual = formatter_utility.show_tables(table_columns)
        self.assertEquals(list(expected), list(actual))

    def test_table_columns_tsv(self):
        """
        Tests `table_columns_tsv`.
        """

        database = 'adipiscing'
        table_columns = ['lorem.ipsum', 'dolor.sit']
        expected = ['adipiscing\tlorem\tipsum', 'adipiscing\tdolor\tsit']
        actual = formatter_utility.table_columns_tsv(database, table_columns)
        self.assertEquals(list(expected), list(actual))

    def test_randomize_queries(self):
        """
        Tests `randomize_queries`.
        """

        queries = ['SELECT NOW()', 'SELECT 1']
        expected = ('SELECT NOW();\n'
                    'SELECT 1;\n')
        actual = formatter_utility.randomize_queries(queries)
        self.assertEquals(expected, actual)

        queries = []
        expected = ''
        actual = formatter_utility.randomize_queries(queries)
        self.assertEquals(expected, actual)

    def test_table_names_from_mydumper_backup(self):
        """
        Tests `table_names_from_mydumper_backup`.
        """

        files = []
        suffixed_database = 'ipsum.'
        actual = formatter_utility.table_names_from_mydumper_backup(files, suffixed_database)
        expected = []
        self.assertTrue(hasattr(actual, 'next') or hasattr(actual, '__next__'))
        self.assertEquals(expected, list(actual))

        files = ['ipsum.dolor.sql', 'ipsum.consectetur.sql']
        suffixed_database = 'ipsum.'
        actual = formatter_utility.table_names_from_mydumper_backup(files, suffixed_database)
        expected = ['dolor', 'consectetur']
        self.assertTrue(hasattr(actual, 'next') or hasattr(actual, '__next__'))
        self.assertEquals(expected, list(actual))

    def test_inclusive_regex_in(self):
        """
        Tests `inclusive_regex_in`.
        """

        inclusive_regex = r'^ipsum\.id$'
        database_table_delimiter = r'\.'
        actual = formatter_utility.inclusive_regex_in(inclusive_regex, database_table_delimiter)
        expected = r'^ipsum', r'id$'
        self.assertEquals(expected, actual)

    def test_inclusive_regex_out(self):
        """
        Tests `inclusive_regex_out`.
        """

        file_basename = 'ipsum'
        field_regex = r'id$'
        database_table_delimiter = r'\.'
        actual = formatter_utility.inclusive_regex_out(file_basename, field_regex, database_table_delimiter)
        expected = r'^ipsum\.id$'
        self.assertEquals(expected, actual)


suite = unittest.TestLoader().loadTestsFromTestCase(TestFormatter)
unittest.TextTestRunner(verbosity=2).run(suite)
