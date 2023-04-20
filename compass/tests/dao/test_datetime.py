# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao import current_datetime, sws_now
from datetime import datetime


class DateTimeFunctionsTest(TestCase):
    def test_current_datetime(self):
        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-05-31 08:00:00'):
            self.assertEqual(current_datetime().strftime('%Y-%m-%d %H:%M:%S'),
                             '2013-05-31 08:00:00')

        with self.settings(CURRENT_DATETIME_OVERRIDE=None):
            self.assertEqual(current_datetime().strftime('%Y-%m-%d %H:%M'),
                             sws_now().strftime('%Y-%m-%d %H:%M'))
