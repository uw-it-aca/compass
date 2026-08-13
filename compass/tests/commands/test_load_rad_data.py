# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from io import StringIO

from django.core.management import call_command

from compass.models.rad_data import CourseAnalyticsScores, RADImport, RADWeek
from compass.tests import CompassTestCase


class TestLoadRadData(CompassTestCase):

    def setUp(self):
        # Required base data
        pass

    def test_first_load(self):
        call_command('load_rad_data')

        # bucket-driven: all fixture files are imported in a single run
        self.assertEqual(RADImport.objects.count(), 11)
        self.assertEqual(
            RADImport.objects.filter(
                import_status=RADImport.SUCCESS).count(), 11)

        # spot-check data for a specific week
        week = RADWeek.objects.get(year=2024, quarter='spring', week=6)
        scores = CourseAnalyticsScores.objects.filter(week=week)
        self.assertEqual(scores.count(), 4)
        self.assertEqual(scores[0].course, 'TRAIN 100 A')
        self.assertEqual(scores[0].prediction_score, 0.0)
        self.assertEqual(scores[2].prediction_score, 1.0)
        self.assertEqual(scores[3].prediction_score, None)

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
        # second call imports all remaining unimported files
        self.assertEqual(RADImport.objects.count(), 11)
        week_5 = RADWeek.objects.get(year=2024, quarter='spring', week=5)
        week_6 = RADWeek.objects.get(year=2024, quarter='spring', week=6)
        self.assertEqual(
            RADImport.objects.get(week=week_6).import_status,
            RADImport.SUCCESS)
        scores = CourseAnalyticsScores.objects.filter(
            week__in=[week_5, week_6])
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
