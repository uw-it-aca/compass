# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao.person import (
    get_students_by_system_keys, get_students_by_student_numbers)
from compass.utils import format_system_key, format_student_number
from compass.exceptions import InvalidCSV
from logging import getLogger
import chardet
import csv
import os

logger = getLogger(__name__)


def normalize(s):
    return s.replace(' ', '').replace('_', '').lower()


class InsensitiveDict(dict):
    """
    Override get() to strip() and lower() the input key, and strip() the
    returned value.
    """
    def get(self, *k, default=None):
        for i in k:
            if normalize(i) in self:
                try:
                    return super().get(normalize(i)).strip()
                except AttributeError:
                    break
        return default


class InsensitiveDictReader(csv.DictReader):
    """
    Override the csv.fieldnames property to strip() and lower() the fieldnames.
    """
    @property
    def fieldnames(self):
        return [normalize(field) for field in super().fieldnames]

    def __next__(self):
        return InsensitiveDict(super().__next__())


class StudentCSV():
    def __init__(self):
        self.encoding = None
        self.has_header = False
        self.dialect = None
        self.student_id_col = None
        self.system_key_cols = ['systemkey', 'syskey']
        self.student_num_cols = ['studentid', 'studentno', 'studentnum',
                                 'studentnumber', 'studentidnumber']

    def decode_file(self, csvfile):
        if not self.encoding:
            result = chardet.detect(csvfile)
            self.encoding = result['encoding']
        return csvfile.decode(self.encoding)

    def validate(self, fileobj):
        # Read the first line of the file to validate the header
        try:
            decoded_file = self.decode_file(fileobj.readline())
            self.has_header = csv.Sniffer().has_header(decoded_file)
            self.dialect = csv.Sniffer().sniff(decoded_file)
        except Exception as err:
            raise InvalidCSV(str(err))

        reader = InsensitiveDictReader(decoded_file.splitlines(),
                                       dialect=self.dialect)

        self.student_id_col = next((
            s for s in (self.system_key_cols + self.student_num_cols) if s in (
                reader.fieldnames)), None)

        if self.student_id_col is None:
            raise InvalidCSV('Missing header row or student identifier')

        fileobj.seek(0, 0)

    def students_from_file(self, fileobj):
        """
        Reads a CSV file object, and returns a list of person JSON objects

        Supported column names are contained in self.system_key_cols and
        self.student_num_cols, with priority given to system_keys.

        All other field names are ignored.
        """
        self.validate(fileobj)
        decoded_file = self.decode_file(fileobj.read()).splitlines()

        student_ids = []
        for row in InsensitiveDictReader(decoded_file, dialect=self.dialect):
            if self.student_id_col in self.system_key_cols:
                student_id = format_system_key(row.get(self.student_id_col))
            else:
                student_id = format_student_number(
                    row.get(self.student_id_col))

            if student_id is not None:
                student_ids.append(student_id)

        students = []
        if len(student_ids):
            if self.student_id_col in self.system_key_cols:
                identifier = 'system_key'
                students_dict = get_students_by_system_keys(student_ids)
            else:
                identifier = 'student_number'
                students_dict = get_students_by_student_numbers(student_ids)

            for sid in student_ids:
                if sid in students_dict:
                    students.append(students_dict[sid])
                else:
                    students.append({
                        identifier: sid,
                        'error': f'Student not found',
                    })

        return students
