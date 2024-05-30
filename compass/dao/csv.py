# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao.person import get_students_by_student_numbers
from compass.utils import format_student_number
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
        self.student_identifiers = [
            'studentid', 'studentno', 'studentnum', 'studentnumber',
            'studentidnumber']

    def decode_file(self, csvfile):
        if not self.encoding:
            result = chardet.detect(csvfile)
            self.encoding = result['encoding']
        return csvfile.decode(self.encoding)

    def validate(self, fileobj):
        # Read the first line of the file to validate the header
        decoded_file = self.decode_file(fileobj.readline())
        self.has_header = csv.Sniffer().has_header(decoded_file)
        self.dialect = csv.Sniffer().sniff(decoded_file)

        reader = InsensitiveDictReader(decoded_file.splitlines(),
                                       dialect=self.dialect)

        if not (any(s in reader.fieldnames for s in self.student_identifiers)):
            raise InvalidCSV('Missing student identifier')

        fileobj.seek(0, 0)

    def students_from_file(self, fileobj):
        """
        Reads a CSV file object, and returns a list of person JSON objects

        Supported column names are contained in self.student_identifiers

        All other field names are ignored.
        """
        self.validate(fileobj)
        decoded_file = self.decode_file(fileobj.read()).splitlines()

        student_numbers = []
        for row in InsensitiveDictReader(decoded_file, dialect=self.dialect):
            student_number = format_student_number(
                row.get(*self.student_identifiers))

            if student_number is not None:
                student_numbers.append(student_number)

        students = []
        if len(student_numbers):
            students_dict = get_students_by_student_numbers(student_numbers)

            for sn in student_numbers:
                if sn in students_dict:
                    students.append(students_dict[sn])
                else:
                    students.append({
                        'student_number': sn,
                        'error': 'Student number not found',
                    })

        return students
