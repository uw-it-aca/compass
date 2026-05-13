# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import CompassTestCase
from compass.dao.visit_file import (validate_visit_upload_file,
                                    _get_datetimes,
                                    _get_student_by_student_number)
from io import BytesIO


class VisitFileDAOFunctionsTest(CompassTestCase):
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
