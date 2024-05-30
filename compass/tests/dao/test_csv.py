# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao.csv import InsensitiveDictReader, StudentCSV
from compass.exceptions import InvalidCSV
from compass.tests import CompassTestCase
import mock
import os


class StudentCSVTest(CompassTestCase):
    def setUp(self):
        self.resource_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'resources', 'csv'))

    def test_validate(self):
        csv_import = StudentCSV()

        with open(os.path.join(self.resource_path, 'valid.csv'), 'rb') as fh:
            r = csv_import.validate(fh)
            self.assertEqual(csv_import.has_header, True)
            self.assertEqual(csv_import.dialect.delimiter, ',')

        with open(os.path.join(
                self.resource_path, 'missing_header.csv'), 'rb') as fh:
            self.assertRaisesRegex(InvalidCSV, 'Missing student identifier',
                                   csv_import.validate, fh)

        with open(os.path.join(
                self.resource_path, 'missing_student_id.csv'), 'rb') as fh:
            self.assertRaisesRegex(InvalidCSV, 'Missing student identifier',
                                   csv_import.validate, fh)

    def test_persons_from_file(self):
        csv_import = StudentCSV()

        with open(os.path.join(self.resource_path, 'valid.csv'), 'rb') as fh:
            result = csv_import.persons_from_file(fh)

            self.assertEqual(len(result), 4)
            self.assertEqual(result[0]['student_number'], '1033334')
            self.assertEqual(result[0]['uwnetid'], 'javerage')
            self.assertEqual(result[1]['student_number'], '1233338')
            self.assertEqual(result[1]['uwnetid'], 'lisa')
            self.assertEqual(result[2]['student_number'], '1233334')
            self.assertEqual(result[2]['uwnetid'], 'jbothell')
            self.assertEqual(result[3]['error'],
                             'Student number 7000000 not found')


class InsensitiveDictReaderTest(StudentCSVTest):
    def test_insensitive_dict_reader(self):
        with open(os.path.join(self.resource_path, 'insensitive.csv')) as fh:
            reader = InsensitiveDictReader(fh)

            row = next(reader)
            self.assertEqual(row.get('Field1'), 'ök1')
            self.assertEqual(row.get('Field2'), 'øk2')
            self.assertEqual(row.get('Field3'), 'ok3')
            self.assertEqual(row.get('Field4'), 'ok4')
            self.assertEqual(row.get('Field 5', 'Field5'), 'ok5')
            self.assertEqual(row.get('Field6', 'field 6'), '')
            self.assertEqual(row.get('Field7'), '')
            self.assertEqual(row.get('Field8'), 'ok_8')
