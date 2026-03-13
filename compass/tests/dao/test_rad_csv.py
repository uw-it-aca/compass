# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.rad_csv import (read_csv, import_data_from_csv,
                                 _parse_score,
                                 get_pred_csv_from_json,
                                 validate_prediction_json)
from compass.models.rad_data import CourseAnalyticsScores, RADWeek
from compass.dao.storage import RADStorageDao


class TestRadCsv(TestCase):

    RAD_FILE = ('compass/fixtures/storage/'
                'compass_data/2024-spring-week-6-compass-data.csv')

    def test_read_csv(self):
        with open(self.RAD_FILE) as f:
            csv_string = f.read()
            data = read_csv(csv_string)
            data_list = list(data)
            self.assertEqual(len(data_list), 4)
            self.assertIn('uw_netid', data_list[0].keys())

    def test_import_from_csv(self):
        with open(self.RAD_FILE) as f:
            csv_string = f.read()
            week = RADWeek.get_or_create_week(year=2024,
                                              quarter='spring',
                                              week=6)
            filename, pred_file = RADStorageDao().get_latest_pred_file()
            import_data_from_csv(week, csv_string, pred_file)
            self.assertEqual(CourseAnalyticsScores.objects.count(), 4)
            self.assertEqual(CourseAnalyticsScores.objects.first().week,
                             week)
            self.assertEqual(CourseAnalyticsScores.objects.first()
                             .assignment_score,
                             3.0)

    def test_parse_score(self):
        self.assertEqual(_parse_score('3.0'), 3.0)
        self.assertEqual(_parse_score('3'), 3.0)
        self.assertEqual(_parse_score(''), 0)
        self.assertEqual(_parse_score(None), 0)

    def test_get_pred_csv_from_json(self):
        sample_json = {
            "body": [
                {
                    "": "0",
                    "system_key": "12345",
                    "student_no": "54321",
                    "uw_netid": "netid123",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                },
                {
                    "": "1",
                    "system_key": "12346",
                    "student_no": "54322",
                    "uw_netid": "netid456",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "True"
                },
                {
                    "": "2",
                    "system_key": "12347",
                    "student_no": "54323",
                    "uw_netid": "netid789",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                }
            ]
        }
        csv_output = get_pred_csv_from_json(sample_json)
        expected_rows = [
            "uw_netid,course_code,pred",
            "netid123,MATH 101 A,False",
            "netid456,MATH 101 A,True",
            "netid789,MATH 101 A,False"
        ]
        expected_csv = "\r\n".join(expected_rows) + "\r\n"

        self.assertEqual(csv_output, expected_csv)

    def test_validate_prediction_json(self):
        valid_json = {
            "body": [
                {
                    "": "0",
                    "system_key": "12345",
                    "student_no": "54321",
                    "uw_netid": "netid123",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                }
            ]
        }
        try:
            validate_prediction_json(valid_json)
        except ValueError:
            self.fail("validate_prediction_json raised ValueError "
                      "unexpectedly!")

        missing_field_json = {
            "body": [
                {
                    "": "0",
                    "system_key": "12345",
                    "student_no": "54321",
                    # Missing uw_netid
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                }
            ]
        }
        with self.assertRaises(ValueError):
            validate_prediction_json(missing_field_json)

        empty_body_json = {
            "body": []
        }
        with self.assertRaises(ValueError):
            validate_prediction_json(empty_body_json)

        no_body_json = {}
        with self.assertRaises(ValueError):
            validate_prediction_json(no_body_json)
