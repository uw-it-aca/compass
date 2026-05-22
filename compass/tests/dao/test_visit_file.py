# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import CompassTestCase
from compass.dao.visit_file import (validate_visit_upload_file,
                                    _get_datetimes,
                                    _get_student_by_student_number,
                                    create_visits_from_file,
                                    get_visit_export)
from compass.models import (AccessGroup,
                            VisitType,
                            VisitTutoringOption,
                            Student,
                            Visit)
from datetime import datetime, timezone
from io import BytesIO


class VisitFileDAOFunctionsTest(CompassTestCase):

    def setUp(self):
        super(VisitFileDAOFunctionsTest, self).setUp()
        ag = AccessGroup(name="OMAD", access_group_id="omad_group")
        ag.save()
        vt = VisitType(name="IC Drop-In Tutoring", access_group=ag)
        vt.save()
        to = VisitTutoringOption(name="Option 1", access_group=ag)
        to.save()

    def test_validate_visit_upload_file_valid(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "12345,Math 101,60\n"
            "67890,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        is_valid, error_message = validate_visit_upload_file(file)
        self.assertTrue(is_valid)
        self.assertEqual(error_message, '')

    def test_validate_visit_upload_file_missing_columns(self):
        csv_content = (
            "student_number,course_name\n"
            "12345,Math 101\n"
            "67890,History 201"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        is_valid, error_message = validate_visit_upload_file(file)
        self.assertFalse(is_valid)
        self.assertIn('Missing required columns', error_message)

    def test_validate_visit_upload_file_missing_data(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "12345,,60\n"
            "67890,History 201,"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        is_valid, error_message = validate_visit_upload_file(file)
        self.assertFalse(is_valid)
        self.assertIn('Missing data in row', error_message)

    def test_validate_visit_upload_file_invalid_duration(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "12345,Math 101,sixty\n"
            "67890,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        is_valid, error_message = validate_visit_upload_file(file)
        self.assertFalse(is_valid)
        self.assertIn('Invalid duration_minutes in row', error_message)

    def test_validate_visit_upload_file_negative_duration(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "12345,Math 101,-30\n"
            "67890,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        is_valid, error_message = validate_visit_upload_file(file)
        self.assertFalse(is_valid)
        self.assertIn('Negative duration_minutes in row', error_message)

    def test_get_datetimes(self):
        duration_minutes = 90
        date = "2024-01-01"
        start_datetime, end_datetime = _get_datetimes(duration_minutes, date)
        self.assertEqual(start_datetime.isoformat(),
                         "2024-01-01T00:00:00")
        self.assertEqual(end_datetime.isoformat(),
                         "2024-01-01T01:30:00")

    def test_get_student_by_student_number(self):
        student = _get_student_by_student_number("1033334")
        self.assertIsNotNone(student)
        self.assertEqual(student.system_key, "532353230")
        with self.assertRaises(ValueError):
            _get_student_by_student_number("9999999")

    def test_create_visits_from_file(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "1033334,Math 101,60\n"
            "1033334,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        num_visits_created = create_visits_from_file(
            file, "IC Drop-In Tutoring", "Option 1", "2024-01-01")
        self.assertEqual(num_visits_created, 2)

    def create_visits_missing_visit_type(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "1033334,Math 101,60\n"
            "1033334,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        with self.assertRaises(ValueError):
            create_visits_from_file(
                file, "Nonexistent Visit Type", "Option 1", "2024-01-01")

    def create_visits_missing_tutoring_option(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "1033334,Math 101,60\n"
            "1033334,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        with self.assertRaises(ValueError):
            create_visits_from_file(
                file, "IC Drop-In Tutoring", "Nonexistent Tutoring Option",
                "2024-01-01")

    def test_bad_student_number(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "9999999,Math 101,60\n"
            "1033334,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        with self.assertRaises(ValueError):
            create_visits_from_file(
                file, "IC Drop-In Tutoring", "Option 1", "2024-01-01")

    def test_visit_export(self):

        student = Student.objects.get_or_create(system_key="12345")[0]
        visit_type = VisitType.objects.get(name="IC Drop-In Tutoring")
        tutoring_option = VisitTutoringOption.objects.get(name="Option 1")

        checkin = datetime(2026, 5, 22, 10, 0, 0, tzinfo=timezone.utc)
        checkout = datetime(2026, 5, 22, 11, 0, 0, tzinfo=timezone.utc)

        Visit.objects.create(
            student=student,
            access_group=visit_type.access_group,
            visit_type=visit_type,
            tutoring_option=tutoring_option,
            course_code="Math 101",
            checkin_date=checkin,
            checkout_date=checkout
        )

        csv_output = get_visit_export()

        expected_csv = (
            "student_syskey,checkin_date,checkout_date,duration_minutes,"
            "visit_type,tutoring_option,course_code\r\n"
            f"12345,{checkin.isoformat()},{checkout.isoformat()},"
            "60,IC Drop-In Tutoring,Option 1,Math 101\r\n"
        )

        self.assertEqual(csv_output, expected_csv)
