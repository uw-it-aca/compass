# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import CompassTestCase
from compass.dao.person import *
from uw_pws.util import fdao_pws_override


@fdao_pws_override
class TestPerson(CompassTestCase):
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

    def test_get_appuser_by_uwnetid(self):
        person = get_appuser_by_uwnetid('bill')
        self.assertEqual(person.uwnetid, 'bill')
        self.assertEqual(person.display_name, 'Bill Average Teacher')
        self.assertEqual(person.student, None)

        self.assertRaises(
            PersonNotFoundException, get_appuser_by_uwnetid, 'nobody')

    def test_get_person_by_uwnetid(self):
        includes = {
            'include_student': True,
            'include_student_holds': True,
            'include_student_transfers': True,
            'include_student_degrees': True,
        }
        person = get_person_by_uwnetid('javerage', **includes)
        self.assertEqual(person.uwnetid, 'javerage')
        self.assertEqual(person.student.student_number, '1033334')
        self.assertEqual(len(person.student.holds.all()), 2)
        self.assertEqual(len(person.student.transfers.all()), 1)
        self.assertEqual(len(person.student.degrees.all()), 1)
        self.assertEqual(person.student.transcripts, None)

    def test_get_person_by_student_number(self):
        includes = {
            'include_student': True,
            'include_student_holds': True,
            'include_student_transfers': True,
            'include_student_degrees': True,
        }
        person = get_person_by_student_number('1033334', **includes)
        self.assertEqual(person.uwnetid, 'javerage')
        self.assertEqual(person.student.student_number, '1033334')
        self.assertEqual(len(person.student.holds.all()), 2)
        self.assertEqual(len(person.student.transfers.all()), 1)
        self.assertEqual(len(person.student.degrees.all()), 1)
        self.assertEqual(person.student.transcripts, None)

    def test_get_person_by_system_key(self):
        includes = {}
        person = get_person_by_system_key('532353230', **includes)
        self.assertEqual(person.uwnetid, 'javerage')
        self.assertEqual(person.system_key, '532353230')

        self.assertRaises(
            PersonNotFoundException, get_person_by_system_key, '111111111')

    def test_get_adviser_caseload_not_found(self):
        self.assertRaises(
            AdviserNotFoundException, get_adviser_caseload, 'javerage')

    def test_get_adviser_caseload(self):
        students = get_adviser_caseload('jadviser')
        s1 = students[0]
        self.assertEqual(s1['surname'], 'Average')

        s2 = students[1]
        self.assertEqual(s2['surname'], 'Student')
