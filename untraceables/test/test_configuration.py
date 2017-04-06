# -*- coding: utf-8 -*-

import os
import unittest

from untraceables.utilities import configuration


class TestConfiguration(unittest.TestCase):

  def test_read_file(self):
    """
    Tests `read_file`.
    """

    filename = 'lorem'
    actual = configuration.read_file(filename)
    self.assertFalse(actual)

    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'untraceables.cfg')
    actual = configuration.read_file(filename)
    expected = 'configobj.ConfigObj'
    self.assertTrue(expected in str(type(actual)))
    expected = 'lorem'
    self.assertEqual(expected, actual['main']['host'])
    expected = 'ipsum'
    self.assertEqual(expected, actual['main']['user'])
    expected = 'dolor'
    self.assertEqual(expected, actual['main']['password'])

  def test_read_file(self):
    """
    Tests `read_xclude_regexes_file`.

    Non existing file.
    """

    expected = []
    actual = configuration.read_xclude_regexes_file('lorem')
    self.assertEqual(expected, actual)

  def test_read_file_0(self):
    """
    Tests `read_xclude_regexes_file`.

    Non-empty file.
    """

    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'include-from-0')
    expected = ['^audit_trails\.user_id$',
                '^audit_trails\..*user_id$',
                '^tickets\.user_id$',
                '^tickets\..*user_id$',
                '^users\.id$',
                '^users\.user_id$',
                '^users\..*user_id$']
    actual = configuration.read_xclude_regexes_file(filename)

  def test_read_file_1(self):
    """
    Tests `read_xclude_regexes_file`.

    Empty file.
    """

    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'include-from-1')
    expected = []
    actual = configuration.read_xclude_regexes_file(filename)


suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
unittest.TextTestRunner(verbosity=2).run(suite)
