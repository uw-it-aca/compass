# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from compass.tests import CompassTestCase
from compass.dao.contact import (
    parse_checkin_date_str, validate_adviser_netid, validate_student_systemkey)


class ContactDaoTest(CompassTestCase):
    def test_parse_checkin_date_str(self):
        # no checkin date specified
        with self.assertRaises(ValueError):
            parse_checkin_date_str(None)
        # bad checkin format
        with self.assertRaises(ValueError):
            parse_checkin_date_str("2022-09-T::")
        # Missing TZ info
        with self.assertRaises(ValueError):
            parse_checkin_date_str("2022-09-19T06:15:04")
        # correct checkin format
        checkin_date = parse_checkin_date_str(
            "2022-09-19T06:15:04Z")
        self.assertEqual(type(checkin_date), datetime)

    def test_validate_adviser_netid(self):
        with self.assertRaises(ValueError):
            validate_adviser_netid(None)
        validate_adviser_netid("foo")

    def test_validate_student_systemkey(self):
        with self.assertRaises(ValueError):
            validate_student_systemkey(None)
        with self.assertRaises(ValueError):
            validate_student_systemkey("badsyskey")
        with self.assertRaises(ValueError):
            validate_student_systemkey(1234)
        validate_student_systemkey("1234")
