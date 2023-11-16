# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.person import is_overridable_uwnetid


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
