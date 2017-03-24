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

suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
unittest.TextTestRunner(verbosity=2).run(suite)
