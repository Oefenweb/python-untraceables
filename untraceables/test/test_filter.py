# -*- coding: utf-8 -*-

import unittest

from untraceables.utilities import filter


class TestFilter(unittest.TestCase):

  def test_show_tables(self):
    """
    Tests `show_tables`.
    """

    table_columns = iter([])
    inclusive_regexes = exclusive_regexes = []
    expected = set([])
    actual = filter.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
    self.assertEquals(expected, actual)

    table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
    inclusive_regexes = exclusive_regexes = []
    expected = set([])
    actual = filter.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
    self.assertEquals(expected, actual)

    table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
    inclusive_regexes = ['^.*\..*$']
    exclusive_regexes = []
    expected = set(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
    actual = filter.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
    self.assertEquals(expected, actual)

    table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
    inclusive_regexes = ['^.*\..*$']
    exclusive_regexes = ['^sit\..*$']
    expected = set(['ipsum.dolor', 'consectetur.adipiscing'])
    actual = filter.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
    self.assertEquals(expected, actual)

    table_columns = iter(['ipsum.dolor', 'sit.amet', 'consectetur.adipiscing'])
    inclusive_regexes = ['^.*\..*$']
    exclusive_regexes = ['^.*\.adipiscing$']
    expected = set(['ipsum.dolor', 'sit.amet'])
    actual = filter.show_tables(table_columns, inclusive_regexes, exclusive_regexes)
    self.assertEquals(expected, actual)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFilter)
unittest.TextTestRunner(verbosity=2).run(suite)