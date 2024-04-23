# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from compass.utils import weekdays_before
from datetime import date


class TestUtils(TestCase):
    def test_weekdays_before(self):
        val = weekdays_before(date(2024, 4, 19), offset_days=3)
        self.assertEqual(str(val), '2024-04-16', 'Friday, offset=3')

        val = weekdays_before(date(2024, 4, 20), offset_days=3)
        self.assertEqual(str(val), '2024-04-17', 'Saturday, offset=3')

        val = weekdays_before(date(2024, 4, 21), offset_days=3)
        self.assertEqual(str(val), '2024-04-17', 'Sunday, offset=3')

        val = weekdays_before(date(2024, 4, 22), offset_days=1)
        self.assertEqual(str(val), '2024-04-19', 'Monday, offset=1')

        val = weekdays_before(date(2024, 4, 22), offset_days=2)
        self.assertEqual(str(val), '2024-04-18', 'Monday, offset=2')

        val = weekdays_before(date(2024, 4, 22), offset_days=3)
        self.assertEqual(str(val), '2024-04-17', 'Monday, offset=3')

        # Bad offsets
        val = weekdays_before(date(2024, 4, 22), offset_days=None)
        self.assertEqual(str(val), '2024-04-22', 'Monday, offset=None')

        val = weekdays_before(date(2024, 4, 22), offset_days=-5)
        self.assertEqual(str(val), '2024-04-22', 'Monday, offset=-5')

        val = weekdays_before(date(2024, 4, 22), offset_days=0)
        self.assertEqual(str(val), '2024-04-22', 'Monday, offset=0')
