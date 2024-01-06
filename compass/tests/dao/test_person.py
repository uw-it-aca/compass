# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.person import *
from uw_pws.util import fdao_pws_override


@fdao_pws_override
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

        err_msg = is_overridable_uwnetid("1javerage")
        self.assertEqual(err_msg, "Not a valid UWNetID: ")

    def test_validation(self):
        self.assertTrue(valid_uwnetid("javerage"))
        self.assertFalse(valid_uwnetid("1javerage"))

        self.assertTrue(valid_uwregid("9136CCB8F66711D5BE060004AC494FFE"))
        self.assertFalse(valid_uwregid("!@#$"))

        self.assertTrue(valid_student_number("1033334"))
        self.assertFalse(valid_student_number("javerage"))

        self.assertTrue(valid_system_key("123456789"))
        self.assertFalse(valid_system_key("javerage"))
