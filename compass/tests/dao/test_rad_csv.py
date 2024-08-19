# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.rad_csv import read_csv, import_data_from_csv
from compass.models.rad_data import RADDataPoint, RADWeek


class TestRadCsv(TestCase):

    RAD_FILE = 'compass/fixtures/rad_data/2024-spring-week-6-compass-data.csv'

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
            import_data_from_csv(week, csv_string)
            self.assertEqual(RADDataPoint.objects.count(), 2)
            self.assertEqual(RADDataPoint.objects.first().week, week)
            self.assertEqual(RADDataPoint.objects.first().assignment_score,
                             3.0)
