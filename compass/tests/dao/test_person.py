# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.person import is_overridable_uwnetid, valid_uwnetid, \
    valid_uwregid, valid_student_number, valid_system_key, person_from_uwnetid
from uw_pws import InvalidNetID


class TestPerson(TestCase):
    def test_is_overridable(self):
        err_msg = is_overridable_uwnetid("javerage")
        self.assertEqual(err_msg, None)

        err_msg = is_overridable_uwnetid(None)
        self.assertEqual(err_msg,
                         "No override user supplied, please enter a UWNetID")

        err_msg = is_overridable_uwnetid("")
        self.assertEqual(err_msg,
                         "No override user supplied, please enter a UWNetID")

        err_msg = is_overridable_uwnetid("javerage1")
        self.assertEqual(err_msg, "UWNetID not found: ")

        err_msg = is_overridable_uwnetid("123invalid$%!@#$")
        self.assertEqual(err_msg, "Not a valid UWNetID: ")

        err_msg = is_overridable_uwnetid("javerage2")
        self.assertEqual(err_msg, "Current netid: javerage, Prior netid: ")

    def test_validation(self):
        self.assertTrue(valid_uwnetid("javerage"))
        self.assertFalse(valid_uwnetid("1javerage"))

        self.assertTrue(valid_uwregid("9136CCB8F66711D5BE060004AC494FFE"))
        self.assertFalse(valid_uwregid("!@#$"))

        self.assertTrue(valid_student_number("1033334"))
        self.assertFalse(valid_student_number("javerage"))

        self.assertTrue(valid_system_key("123456789"))
        self.assertFalse(valid_system_key("javerage"))

    def test_person_from_uwnetid(self):
        self.assertRaises(InvalidNetID, person_from_uwnetid, "1javerage")
        self.assertIsNotNone(person_from_uwnetid("javerage"))
