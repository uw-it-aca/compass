# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import reverse
from compass.tests import CompassTestCase
from compass.dao.person import *
from uw_pws.util import fdao_pws_override
import mock


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
            'include_student_transcripts': True,
            'include_student_degrees': True,
        }
        person = get_person_by_uwnetid('javerage', **includes)
        self.assertEqual(person.uwnetid, 'javerage')
        self.assertEqual(person.student.student_number, '1033334')
        self.assertEqual(len(person.student.holds.all()), 2)
        self.assertEqual(len(person.student.transfers.all()), 1)
        self.assertEqual(len(person.student.transcripts.all()), 2)
        self.assertEqual(len(person.student.degrees.all()), 1)

    def test_get_person_by_uwregid(self):
        includes = {
            'include_student': True,
            'include_student_holds': True,
            'include_student_transfers': True,
            'include_student_transcripts': True,
            'include_student_degrees': True,
        }
        person = get_person_by_uwregid('9136CCB8F66711D5BE060004AC494FFE',
                                       **includes)
        self.assertEqual(person.uwnetid, 'javerage')
        self.assertEqual(person.student.student_number, '1033334')
        self.assertEqual(len(person.student.holds.all()), 2)
        self.assertEqual(len(person.student.transfers.all()), 1)
        self.assertEqual(len(person.student.transcripts.all()), 2)
        self.assertEqual(len(person.student.degrees.all()), 1)

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

    def test_get_transcripts_by_uwregid(self):
        self.assertRaises(PersonNotFoundException,
                          get_transcripts_by_uwregid,
                          '11111111EEEEEEEEBBBBBBBB00000000')

        transcripts = get_transcripts_by_uwregid(
            'FBB38FE46A7C11D5A4AE0004AC494FFE')
        self.assertEqual(len(transcripts), 0)

        transcripts = get_transcripts_by_uwregid(
            '9136CCB8F66711D5BE060004AC494FFE')
        self.assertEqual(len(transcripts), 2)

        # default transcript sorting
        t1 = transcripts[0]
        t2 = transcripts[1]
        self.assertLess(int(f'{t2.tran_term.year}{t2.tran_term.quarter}'),
                        int(f'{t1.tran_term.year}{t1.tran_term.quarter}'))

    @mock.patch.object(PhotoDAO, 'generate_photo_key')
    def test_get_students_by_system_keys(self, mock_photo_key):
        key = 'testtesttesttest'
        mock_photo_key.return_value = key

        system_keys = ['532353230', '820582050', '888777333']
        students = get_students_by_system_keys(system_keys)

        self.assertEqual(len(students), 3)

        s1 = students['532353230']
        self.assertEqual(s1['display_name'], 'Jamesy McJamesy')
        self.assertEqual(s1['photo_url'], reverse('photo', kwargs={
            'uwregid': s1['person__uwregid'], 'photo_key': key}))
        self.assertEqual(len(s1['adviser_uwnetids']), 1)

        s2 = students['820582050']
        self.assertEqual(s2['display_name'], 'James Bothell Student')
        self.assertEqual(s2['photo_url'], reverse('photo', kwargs={
            'uwregid': s2['person__uwregid'], 'photo_key': key}))
        self.assertEqual(len(s2['adviser_uwnetids']), 1)

        s3 = students['888777333']
        self.assertEqual(s3['display_name'], 'Lisa Simpson')
        self.assertEqual(s3['photo_url'], reverse('photo', kwargs={
            'uwregid': s3['person__uwregid'], 'photo_key': key}))
        self.assertEqual(len(s3['adviser_uwnetids']), 2)

    @mock.patch.object(PhotoDAO, 'generate_photo_key')
    def test_get_adviser_caseload_not_found(self, mock_photo_key):
        self.assertRaises(
            AdviserNotFoundException, get_adviser_caseload, 'javerage')

    @mock.patch.object(PhotoDAO, 'generate_photo_key')
    def test_get_adviser_caseload(self, mock_photo_key):
        key = 'testtesttesttest'
        mock_photo_key.return_value = key

        students = get_adviser_caseload('jadviser')
        self.assertEqual(len(students), 3)

        s1 = students[0]
        self.assertEqual(s1['display_name'], 'Jamesy McJamesy')
        self.assertEqual(s1['photo_url'], reverse('photo', kwargs={
            'uwregid': s1['uwregid'], 'photo_key': key}))

        s2 = students[1]
        self.assertEqual(s2['display_name'], 'Lisa Simpson')
        self.assertEqual(s2['photo_url'], reverse('photo', kwargs={
            'uwregid': s2['uwregid'], 'photo_key': key}))

        s3 = students[2]
        self.assertEqual(s3['display_name'], 'James Bothell Student')
        self.assertEqual(s3['photo_url'], reverse('photo', kwargs={
            'uwregid': s3['uwregid'], 'photo_key': key}))
