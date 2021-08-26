# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
import unittest
from django.test import TestCase
from compass import utilities


class TestUtilities(TestCase):

    def test_datestring_to_datetime(self):
        # bad input string
        with self.assertRaises(ValueError):
            utilities.datestring_to_datetime("Bad string")

        # bad input not string or unicode
        with self.assertRaises(ValueError):
            utilities.datestring_to_datetime(int(19))

        # %Y-%m-%dT%H:%M:%S.%f good
        ret = utilities.datestring_to_datetime(
            "2019-01-01T23:59:59.999")
        self.assertTrue(ret)
        self.assertTrue(type(ret) is datetime.datetime)

        # %Y-%m-%dT%H:%M:%S.%f < 1900
        with self.assertRaises(ValueError):
            ret = utilities.datestring_to_datetime(
                "1777-01-01T23:59:59.999")

        # %Y-%m-%dT%H:%M:%S.%fZ good
        ret = utilities.datestring_to_datetime(
            "2019-01-01T23:59:59.999Z")
        self.assertTrue(ret)
        self.assertTrue(type(ret) is datetime.datetime)

        # %Y-%m-%dT%H:%M:%S.%fZ < 1900
        with self.assertRaises(ValueError):
            ret = utilities.datestring_to_datetime(
                "1777-01-01T23:59:59.999Z")

        # %Y-%m-%dT%H:%M:%S good
        ret = utilities.datestring_to_datetime(
            "2019-01-01T23:59:59")
        self.assertTrue(ret)
        self.assertTrue(type(ret) is datetime.datetime)

        # %Y-%m-%dT%H:%M:%S < 1900
        with self.assertRaises(ValueError):
            ret = utilities.datestring_to_datetime(
                "1777-01-01T23:59:59")

        # %Y-%m-%dT%H:%M:%SZ good
        ret = utilities.datestring_to_datetime(
            "2019-01-01T23:59:59Z")
        self.assertTrue(ret)
        self.assertTrue(type(ret) is datetime.datetime)

        # %Y-%m-%dT%H:%M:%SZ < 1900
        with self.assertRaises(ValueError):
            ret = utilities.datestring_to_datetime(
                "1777-01-01T23:59:59Z")

        # already a datetime object
        ret1 = utilities.datestring_to_datetime(ret)
        self.assertEqual(ret1, ret)

    def test_get_term_number(self):
        self.assertEqual(utilities.get_term_number("winter"), 1)
        self.assertEqual(utilities.get_term_number("spring"), 2)
        self.assertEqual(utilities.get_term_number("summer"), 3)
        self.assertEqual(utilities.get_term_number("autumn"), 4)
        with self.assertRaises(ValueError):
            utilities.get_term_number("bad-term")


if __name__ == "__main__":
    unittest.main()
