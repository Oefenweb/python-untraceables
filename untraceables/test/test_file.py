# -*- coding: utf-8 -*-

import os
import unittest

from untraceables.utilities import file as file_utility


class TestFile(unittest.TestCase):

  def test_get_sorted_file_list(self):
    """
    Tests `get_sorted_file_list`.
    """

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    expected = ['include-from-0', 'include-from-1',
                'test_split_file_0.sql', 'test_split_file_1.sql', 'test_split_file_2.sql',
                'untraceables.cfg']
    actual = file_utility.get_sorted_file_list(path)
    self.assertEquals(expected, list(actual))

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data-non-existing')
    expected = []
    actual = file_utility.get_sorted_file_list(path)
    self.assertEquals(expected, list(actual))

suite = unittest.TestLoader().loadTestsFromTestCase(TestFile)
unittest.TextTestRunner(verbosity=2).run(suite)
