# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import date, datetime, timedelta, timezone
from io import BytesIO

from django.conf import settings
from django.test import override_settings
from django.utils import timezone as django_timezone

from compass.dao.visit_file import (
    _get_datetimes,
    _get_student_by_student_number,
    create_visits_from_file,
    get_visit_export,
    validate_visit_upload_file,
)
from compass.models import AccessGroup, Student, Visit, VisitTutoringOption, VisitType
from compass.tests import CompassTestCase


class VisitFileDAOFunctionsTest(CompassTestCase):

    def setUp(self):
        super().setUp()
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

    @override_settings(TIME_ZONE='UTC')
    def test_get_datetimes(self):
        duration_minutes = 90
        date = "2024-01-01"
        start_datetime, end_datetime = _get_datetimes(duration_minutes, date)
        self.assertEqual(start_datetime.isoformat(),
                         "2024-01-01T00:00:00+00:00")
        self.assertEqual(end_datetime.isoformat(),
                         "2024-01-01T01:30:00+00:00")

    @override_settings(TIME_ZONE='America/Los_Angeles')
    def test_get_datetimes_preserves_elapsed_duration_across_dst(self):
        for visit_date in ('2026-03-08', '2026-11-01'):
            with self.subTest(date=visit_date):
                start, end = _get_datetimes(180, visit_date)
                self.assertEqual(
                    django_timezone.localtime(start).isoformat()[:19],
                    f'{visit_date}T00:00:00')
                self.assertEqual((end - start).total_seconds(), 180 * 60)

    @override_settings(TIME_ZONE='America/Los_Angeles')
    def test_import_exports_on_selected_local_date(self):
        for visit_date in ('2026-01-01', '2026-10-01'):
            with self.subTest(date=visit_date):
                file = BytesIO(
                    b'student_number,course_name,duration_minutes\n'
                    b'1033334,Month Boundary,60\n')
                create_visits_from_file(
                    file, 'IC Drop-In Tutoring', 'Option 1', visit_date)
                selected_date = date.fromisoformat(visit_date)
                output = ''.join(get_visit_export(
                    selected_date, selected_date))
                self.assertEqual(len(output.splitlines()), 2)
                self.assertIn(',60,IC Drop-In Tutoring,Option 1,', output)
                previous_date = selected_date - timedelta(days=1)
                self.assertNotIn('Month Boundary', ''.join(
                    get_visit_export(previous_date, previous_date)))

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

    def test_create_visits_missing_visit_type(self):
        csv_content = (
            "student_number,course_name,duration_minutes\n"
            "1033334,Math 101,60\n"
            "1033334,History 201,45"
        )
        file = BytesIO(csv_content.encode('utf-8'))
        with self.assertRaises(ValueError):
            create_visits_from_file(
                file, "Nonexistent Visit Type", "Option 1", "2024-01-01")

    def test_create_visits_missing_tutoring_option(self):
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
        compass_access_group_name = settings.COMPASS_VISITS_ACCESS_GROUP_NAME
        compass_access_group = AccessGroup.objects.get(
            name=compass_access_group_name)

        checkin_2 = datetime(2026, 5, 22, 10, 0, 0, tzinfo=timezone.utc)
        checkout_2 = datetime(2026, 5, 22, 11, 0, 0, tzinfo=timezone.utc)
        checkin_1 = datetime(2026, 5, 21, 10, 0, 0, tzinfo=timezone.utc)
        checkout_1 = datetime(2026, 5, 21, 10, 30, 0, tzinfo=timezone.utc)

        Visit.objects.create(
            student=student,
            access_group=compass_access_group,
            visit_type=visit_type,
            tutoring_option=tutoring_option,
            course_code="Math 100",
            checkin_date=checkin_1,
            checkout_date=checkout_1
        )

        Visit.objects.create(
            student=student,
            access_group=compass_access_group,
            visit_type=visit_type,
            tutoring_option=tutoring_option,
            course_code="Math 101",
            checkin_date=checkin_2,
            checkout_date=checkout_2
        )

        other_ag = AccessGroup.objects.create(
            name="Other Group", access_group_id="other_group")
        other_visit_type = VisitType.objects.create(
            name="Other Visit Type", access_group=other_ag)
        other_tutoring_option = VisitTutoringOption.objects.create(
            name="Other Option", access_group=other_ag)
        Visit.objects.create(
            student=student,
            access_group=other_ag,
            visit_type=other_visit_type,
            tutoring_option=other_tutoring_option,
            course_code="Should Not Export",
            checkin_date=datetime(2026, 5, 20, 10, 0, 0, tzinfo=timezone.utc),
            checkout_date=datetime(2026, 5, 20, 11, 0, 0, tzinfo=timezone.utc)
        )

        csv_output = ''.join(get_visit_export())

        expected_csv = (
            "student_syskey,checkin_date,checkout_date,duration_minutes,"
            "visit_type,tutoring_option,course_code\r\n"
            f"12345,{checkin_1.isoformat()},{checkout_1.isoformat()},"
            "30,IC Drop-In Tutoring,Option 1,Math 100\r\n"
            f"12345,{checkin_2.isoformat()},{checkout_2.isoformat()},"
            "60,IC Drop-In Tutoring,Option 1,Math 101\r\n"
        )

        self.assertEqual(csv_output, expected_csv)

        with self.settings(TIME_ZONE='UTC'):
            filtered_csv = ''.join(get_visit_export(
                date(2026, 5, 22), date(2026, 5, 22)))
            self.assertNotIn('Math 100', filtered_csv)
            self.assertIn('Math 101', filtered_csv)
            self.assertNotIn('Should Not Export', filtered_csv)
            self.assertEqual(len(filtered_csv.splitlines()), 2)
