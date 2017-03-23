# -*- coding: utf-8 -*-

import unittest

from untraceables.utilities import validation


class TestValidation(unittest.TestCase):

  def test_check_max_ids(self):
    """
    Tests `check_max_ids`.
    """

    max_id = mapping_max_id = None
    actual = validation.check_max_ids(max_id, mapping_max_id)
    self.assertTrue(actual)

    max_id = 10
    mapping_max_id = None
    actual = validation.check_max_ids(max_id, mapping_max_id)
    self.assertTrue(actual)

    max_id = 10
    mapping_max_id = 9
    actual = validation.check_max_ids(max_id, mapping_max_id)
    self.assertTrue(actual)

    max_id = 10
    mapping_max_id = 10
    actual = validation.check_max_ids(max_id, mapping_max_id)
    self.assertFalse(actual)

    max_id = None
    mapping_max_id = 10
    actual = validation.check_max_ids(max_id, mapping_max_id)
    self.assertFalse(actual)

suite = unittest.TestLoader().loadTestsFromTestCase(TestValidation)
unittest.TextTestRunner(verbosity=2).run(suite)