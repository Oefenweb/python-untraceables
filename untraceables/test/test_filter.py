# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest
from untraceables.utilities import filter as filter_utility


class TestFilter(unittest.TestCase):

    def test_show_tables(self):
        """
        Tests `show_tables`.
        """

        table_columns = iter([])
        inclusive_regexes = exclusive_regexes = []
        expected = set([])
        actual = filter_utility.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
        self.assertEquals(expected, actual)

        table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
        inclusive_regexes = exclusive_regexes = []
        expected = set([])
        actual = filter_utility.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
        self.assertEquals(expected, actual)

        table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
        inclusive_regexes = [r'^.*\..*$']
        exclusive_regexes = []
        expected = set(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
        actual = filter_utility.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
        self.assertEquals(expected, actual)

        table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
        inclusive_regexes = [r'^.*\..*$']
        exclusive_regexes = [r'^sit\..*$']
        expected = set(['ipsum.dolor', 'consectetur.adipiscing'])
        actual = filter_utility.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
        self.assertEquals(expected, actual)

        table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
        inclusive_regexes = [r'^.*\..*$']
        exclusive_regexes = [r'^.*\.adipiscing$']
        expected = set(['ipsum.dolor', 'sit.amet'])
        actual = filter_utility.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
        self.assertEquals(expected, actual)

    def test_table_names_from_mydumper_backup(self):
        """
        Tests `table_names_from_mydumper_backup`.
        """

        files = []
        suffixed_database = 'ipsum.'
        expected = []
        actual = filter_utility.table_names_from_mydumper_backup(files, suffixed_database)
        self.assertTrue(hasattr(actual, 'next') or hasattr(actual, '__next__'))
        self.assertEquals(expected, list(actual))

        files = ['ipsum.dolor-schema.sql', 'ipsum.dolor.sql',
                 'ipsum.consectetur-schema.sql', 'ipsum.consectetur.sql',
                 'ipsum-schema-create.sql', 'ipsum.sit-schema.sql', 'ipsum.sit.00000.sql']
        suffixed_database = 'ipsum.'
        expected = ['ipsum.dolor.sql', 'ipsum.consectetur.sql', 'ipsum.sit.00000.sql']
        actual = filter_utility.table_names_from_mydumper_backup(files, suffixed_database)
        self.assertTrue(hasattr(actual, 'next') or hasattr(actual, '__next__'))
        self.assertEquals(expected, list(actual))

        files = ['ipsum.dolor-schema.sql', 'ipsum.dolor.sql',
                 'ipsum-schema-create.sql', 'ipsum.sit-schema.sql', 'ipsum.sit.00000.sql',
                 'consectetur.adipiscing-schema.sql', 'consectetur.adipiscing.sql',
                 'elit-schema-create.sql', 'elit.mollis-schema.sql', 'elit.mollis.00000.sql']
        suffixed_database = 'ipsum.'
        expected = ['ipsum.dolor.sql', 'ipsum.sit.00000.sql']
        actual = filter_utility.table_names_from_mydumper_backup(files, suffixed_database)
        self.assertEquals(expected, list(actual))


suite = unittest.TestLoader().loadTestsFromTestCase(TestFilter)
unittest.TextTestRunner(verbosity=2).run(suite)
