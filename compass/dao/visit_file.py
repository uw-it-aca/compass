# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
from io import StringIO
from datetime import datetime, timedelta

from compass.models import (Visit,
                            Student,
                            VisitTutoringOption,
                            VisitType)

from compass.dao.person import get_person_by_student_number
from compass.dao.compass_visits import get_compass_visits_access_group


def validate_visit_upload_file(file):
    """
    Validates the uploaded visit file.
    CSV should have the following columns with data for each row:
    student_number, course_name, duration_minutes
    returns tuple of (is_valid, error_message)
    """
    required_columns = {'student_number', 'course_name', 'duration_minutes'}
    try:
        decoded_file = file.read().decode('utf-8')
        csv_file = StringIO(decoded_file)
        reader = csv.DictReader(csv_file)
        if not required_columns.issubset(reader.fieldnames):
            missing = required_columns - set(reader.fieldnames)
            return (False, f'Missing required columns: {", ".join(missing)}')
        for i, row in enumerate(reader, start=1):
            if not row['student_number'].strip() \
                or not row['course_name'].strip() \
                    or not row['duration_minutes'].strip():
                return (False, f'Missing data in row {i}')
            try:
                int(row['duration_minutes'])
                if int(row['duration_minutes']) < 0:
                    return (False, f'Negative duration_minutes in row {i}')
            except ValueError:
                return (False, f'Invalid duration_minutes in row {i}')
    except Exception as e:
        return (False, f'Error processing file: {str(e)}')
    return (True, '')


def create_visits_from_file(file, visit_type, tutoring_option, date):
    """
    Creates Visit records from the validated file.
    Returns the number of visits created.

    """
    access_group = get_compass_visits_access_group()
    csv_file = file.read().decode('utf-8')
    reader = csv.DictReader(StringIO(csv_file))
    try:
        visit_type_obj = VisitType.objects.get(name=visit_type,
                                               access_group=access_group)
        tutoring_option_obj = VisitTutoringOption.objects.get(
            name=tutoring_option, access_group=access_group)
    except VisitType.DoesNotExist:
        raise ValueError(f'VisitType "{visit_type}" does not exist for'
                         f' access group "{access_group.name}"')
    except VisitTutoringOption.DoesNotExist:
        raise ValueError(f'VisitTutoringOption "{tutoring_option}" does not'
                         f' exist for access group "{access_group.name}"')

    visit_objects = []

    for row in reader:
        student = _get_student_by_student_number(row['student_number'])
        start_datetime, end_datetime = _get_datetimes(
            int(row['duration_minutes']), date)
        visit = Visit(
            student=student,
            access_group=access_group,
            visit_type=visit_type_obj,
            tutoring_option=tutoring_option_obj,
            course_code=row['course_name'],
            checkin_date=start_datetime,
            checkout_date=end_datetime
        )
        visit_objects.append(visit)
    Visit.objects.bulk_create(visit_objects)
    return len(visit_objects)


def _get_datetimes(duration_minutes, date):
    """
    Calculate start and end datetimes based on duration and date string.
    Returns a tuple of (start_datetime, end_datetime)
    """

    start_datetime = datetime.strptime(date, "%Y-%m-%d")
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)
    return start_datetime, end_datetime


def _get_student_by_student_number(student_number):
    try:
        person = get_person_by_student_number(student_number)
        student = Student.objects.get_or_create(
            system_key=person.system_key)[0]
        return student
    except Exception as e:
        raise ValueError(f'Error retrieving student'
                         f' with number {student_number}: {e}')
