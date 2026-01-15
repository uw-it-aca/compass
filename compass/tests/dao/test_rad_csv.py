# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.rad_csv import (read_csv, import_data_from_csv,
                                 _parse_score, validate_prediction_csv)
from compass.models.rad_data import CourseAnalyticsScores, RADWeek
from compass.dao.storage import RADStorageDao


class TestRadCsv(TestCase):

    RAD_FILE = ('compass/fixtures/'
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
            with open('compass/fixtures/sample_azure_pred_file.csv') as f:
                pred_file = f.read()
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

    def test_validate_prediction_csv(self):
        sample_csv = """
        ,system_key,student_no,uw_netid,yrq,course_code,pred
        0,0000001,8123456,javerage  ,20252,TRAIN 100 A,False
        1,0000002,1000002,jsmith    ,20252,BIOL 101 A,True
        2,0000003,8654321,lisa      ,20252,TRAIN 100 A,False
        """
        sample_csv = "\n".join([line.strip() for line in sample_csv.strip()
                               .split("\n")])
        self.assertTrue(validate_prediction_csv(sample_csv))

        no_rows = """
        ,system_key,student_no,uw_netid,yrq,course_code,pred
        """
        no_rows = "\n".join([line.strip() for line in no_rows.strip()
                            .split("\n")])
        with self.assertRaises(ValueError):
            validate_prediction_csv(no_rows)

        missing_field = """
        ,system_key,student_no,uw_netid,yrq,course_code
        0,0000001,8123456,javerage  ,20252,TRAIN 100 A
        """
        missing_field = "\n".join([line.strip() for line in missing_field
                                  .strip().split("\n")])
        with self.assertRaises(ValueError):
            validate_prediction_csv(missing_field)
