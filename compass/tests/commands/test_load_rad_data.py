# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from io import StringIO
from django.core.management import call_command
from compass.tests import CompassTestCase
from compass.models.rad_data import RADWeek, RADImport, CourseAnalyticsScores


class TestLoadRadData(CompassTestCase):

    def setUp(self):
        # Required base data
        pass

    def test_first_load(self):
        call_command('load_rad_data')

        self.assertEqual(RADWeek.objects.count(), 1)
        week = RADWeek.objects.first()
        self.assertEqual(week.year, 2024)
        self.assertEqual(week.quarter, 'spring')
        self.assertEqual(week.week, 6)

        self.assertEqual(RADImport.objects.count(), 1)
        rad_import = RADImport.objects.first()
        self.assertEqual(rad_import.week, week)
        self.assertEqual(rad_import.import_status, RADImport.SUCCESS)

        self.assertEqual(CourseAnalyticsScores.objects.count(), 4)
        scores = CourseAnalyticsScores.objects.all()
        self.assertEqual(scores[0].course, 'TRAIN 100 A')

    def test_load_specific_week(self):
        call_command('load_rad_data', week='2024-spring-week-5')
        self.assertEqual(RADWeek.objects.count(), 1)
        week = RADWeek.objects.first()
        self.assertEqual(week.year, 2024)
        self.assertEqual(week.quarter, 'spring')
        self.assertEqual(week.week, 5)

        self.assertEqual(RADImport.objects.count(), 1)
        rad_import = RADImport.objects.first()
        self.assertEqual(rad_import.week, week)
        self.assertEqual(rad_import.import_status, RADImport.SUCCESS)

        self.assertEqual(CourseAnalyticsScores.objects.count(), 2)
        scores = CourseAnalyticsScores.objects.all()
        self.assertEqual(scores[0].course, 'CHEM 132 A')

    def test_load_next_week(self):
        call_command('load_rad_data', week='2024-spring-week-5')
        call_command('load_rad_data')
        self.assertEqual(RADWeek.objects.count(), 2)
        week = RADWeek.objects.last()
        self.assertEqual(week.week, 6)
        scores = CourseAnalyticsScores.objects.all()
        self.assertEqual(len(scores), 6)

    def test_reload(self):
        call_command('load_rad_data', week='2024-spring-week-5')
        self.assertEqual(RADImport.objects.count(), 1)

        stdout = StringIO()
        call_command('load_rad_data', week='2024-spring-week-5',
                     stdout=stdout)
        self.assertEqual(stdout.getvalue(),
                         'Import already exists for 2024-spring-week-5\n')
        self.assertEqual(RADImport.objects.count(), 1)

        call_command('load_rad_data', week='2024-spring-week-5',
                     reload=True)
        self.assertEqual(RADImport.objects.count(), 1)

    def test_loadall_reload(self):
        call_command('load_rad_data', week='2024-spring-week-5')
        call_command('load_rad_data', week='2024-spring-week-6')
        self.assertEqual(RADImport.objects.count(), 2)
        stdout = StringIO()
        call_command('load_rad_data',
                     loadall=True,
                     stdout=stdout)
        self.assertEqual(RADImport.objects.count(), 11)
        err_str = ("Import already exists for 2024-spring-week-6\n"
                   "Import already exists for 2024-spring-week-5\n")

        # order of errors is not guaranteed
        has_both_errors = (("already exists for 2024-spring-week-6"
                            in err_str)
                           and ("already exists for 2024-spring-week-5"
                                in err_str))
        self.assertTrue(has_both_errors)

        stdout = StringIO()
        call_command('load_rad_data',
                     loadall=True,
                     reload=True,
                     stdout=stdout)
        self.assertEqual(RADImport.objects.count(), 11)
        self.assertEqual(stdout.getvalue(), "")

    def test_loadall(self):
        call_command('load_rad_data', loadall=True)
        self.assertEqual(RADImport.objects.count(), 11)
