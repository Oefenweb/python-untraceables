# -*- coding: utf-8 -*-

import os
import unittest

from untraceables.utilities import configuration as configuration_utility


class TestConfiguration(unittest.TestCase):

    def test_read_file(self):
        """
        Tests `read_file`.
        """

        filename = 'lorem'
        actual = configuration_utility.read_file(filename)
        self.assertFalse(actual)

        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'untraceables.cfg')
        actual = configuration_utility.read_file(filename)
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

        Non-existing file.
        """

        expected = []
        actual = configuration_utility.read_xclude_regexes_file('lorem')
        self.assertEqual(expected, actual)

    def test_read_file_0(self):
        """
        Tests `read_xclude_regexes_file`.

        Non-empty file.
        """

        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'include-from-0')
        expected = [r'^audit_trails\.user_id$',
                    r'^audit_trails\..*user_id$',
                    r'^tickets\.user_id$',
                    r'^tickets\..*user_id$',
                    r'^users\.id$',
                    r'^users\.user_id$',
                    r'^users\..*user_id$']
        actual = configuration_utility.read_xclude_regexes_file(filename)

    def test_read_file_1(self):
        """
        Tests `read_xclude_regexes_file`.

        Empty file.
        """

        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'include-from-1')
        expected = []
        actual = configuration_utility.read_xclude_regexes_file(filename)


suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
unittest.TextTestRunner(verbosity=2).run(suite)
