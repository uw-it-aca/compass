# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
from io import StringIO


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
