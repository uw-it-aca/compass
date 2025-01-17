# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.rad_csv import read_csv, import_data_from_csv, _parse_score
from compass.models.rad_data import CourseAnalyticsScores, RADWeek
from compass.dao.storage import RADStorageDao


class TestRadCsv(TestCase):

    RAD_FILE = ('compass/fixtures/'
                'compass_data/2024-spring-week-6-compass-data.csv')

    def test_read_csv(self):
        with open(self.RAD_FILE) as f:
            csv_string = f.read()
            data = read_csv(csv_string)
            self.assertEqual(len(data), 2)
            self.assertIn('uw_netid', data[0].keys())

    def test_import_from_csv(self):
        with open(self.RAD_FILE) as f:
            csv_string = f.read()
            week = RADWeek.get_or_create_week(year=2024,
                                              quarter='spring',
                                              week=6)
            pred_file = (RADStorageDao().
                         get_pred_file_by_y_q_w(week.year,
                                                week.quarter,
                                                week.week))
            import_data_from_csv(week, csv_string, pred_file)
            self.assertEqual(CourseAnalyticsScores.objects.count(), 2)
            self.assertEqual(CourseAnalyticsScores.objects.first().week, week)
            self.assertEqual(CourseAnalyticsScores.objects.first()
                             .assignment_score,
                             3.0)

    def test_parse_score(self):
        self.assertEqual(_parse_score('3.0'), 3.0)
        self.assertEqual(_parse_score('3'), 3.0)
        self.assertEqual(_parse_score(''), 0)
        self.assertEqual(_parse_score(None), 0)
