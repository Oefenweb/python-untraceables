# -*- coding: utf-8 -*-

"""
Validation utility functions.
"""


def check_max_ids(max_id, mapping_max_id):
    """
    Checks that the maximum ID of the mapping table is sufficient.

    :type long
    :param max_id: The maximum id
    :type long
    :param mapping_max_id: The maximum id of the mapping table
    :rtype bool
    :return Failure
    """

    return mapping_max_id is None or (max_id is not None and mapping_max_id < max_id)
