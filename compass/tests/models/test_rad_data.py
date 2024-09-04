# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import random
from compass.tests import CompassTestCase
from compass.models.rad_data import RADWeek, RADImport, CourseAnalyticsScores


class RADDataWeekTest(CompassTestCase):
    def test_create_week(self):
        week1 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=10)
        self.assertIsNotNone(week1)
        self.assertEqual(week1.year, 2021)
        self.assertEqual(week1.quarter, 'spring')
        self.assertEqual(week1.week, 10)
        self.assertEqual(week1.key, 2021210)
        week2 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=10)
        self.assertEqual(week2.key, 2021210)
        self.assertEqual(week2.id, week1.id)

    def test_week_padding(self):
        week1 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=1)
        self.assertEqual(week1.key, 2021201)
        week2 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=10)
        self.assertEqual(week2.key, 2021210)

    def test_get_next(self):
        spr_week = RADWeek.get_or_create_week(year=2021,
                                              quarter='spring',
                                              week=10)
        aut_week = RADWeek.get_or_create_week(year=2021,
                                              quarter='autumn',
                                              week=5)

        self.assertEqual(spr_week.get_next_quarter(), 'summer')
        self.assertEqual(aut_week.get_next_quarter(), 'winter')

    def test_get_next_week(self):
        w1 = RADWeek.get_or_create_week(year=2021,
                                        quarter='spring',
                                        week=10)
        w2 = RADWeek.get_or_create_week(year=2021,
                                        quarter='autumn',
                                        week=10)
        RADImport.objects.create(week=w1,
                                 import_status=RADImport.STARTED)

        year, quarter, week = RADImport.get_next_import_week()
        self.assertEqual(year, 2021)
        self.assertEqual(quarter, 'summer')
        self.assertEqual(week, 1)
        RADImport.objects.create(week=w2,
                                 import_status=RADImport.STARTED)
        year, quarter, week = RADImport.get_next_import_week()
        self.assertEqual(year, 2022)
        self.assertEqual(quarter, 'winter')
        self.assertEqual(week, 1)

    def test_create_job(self):
        rad_import = RADImport.create_job(year=2021,
                                          quarter='spring',
                                          week=10)
        self.assertEqual(rad_import.week.year, 2021)
        with self.assertRaises(ValueError):
            RADImport.create_job(year=2021,
                                 quarter='spring',
                                 week=10)
        RADImport.create_job(year=2021,
                             quarter='spring',
                             week=10,
                             reload=True)


class CourseAnalyticsScoresTest(CompassTestCase):

    def setUp(self):
        data_points = []
        for week_id in range(10):
            terms = ['spring', 'summer', 'autumn']
            for term in terms:
                week = RADWeek.get_or_create_week(year=2021,
                                                  quarter=term,
                                                  week=week_id)
                data_points.append(
                    CourseAnalyticsScores(
                        uwnetid="javerage",
                        course="CSE 142 A",
                        week=week,
                        activity_score=random.uniform(0, 5),
                        assignment_score=random.uniform(0, 5),
                        grade_score=random.uniform(0, 5),
                        prediction_score=random.uniform(0, 5),
                        signin_score=random.uniform(0, 5)
                    )
                )
                data_points.append(
                    CourseAnalyticsScores(
                        uwnetid="javerage",
                        course="BIO 120 C",
                        week=week,
                        activity_score=random.uniform(0, 5),
                        assignment_score=random.uniform(0, 5),
                        grade_score=random.uniform(0, 5),
                        prediction_score=random.uniform(0, 5),
                        signin_score=random.uniform(0, 5)
                    )
                )
        CourseAnalyticsScores.objects.bulk_create(data_points)

    def test_get_recent_week(self):
        recent_week = RADWeek.get_most_recent_week()
        self.assertEqual(recent_week.year, 2021)
        self.assertEqual(recent_week.quarter, 'autumn')
        self.assertEqual(recent_week.week, 9)

    def test_previous_term(self):
        self.assertEqual(RADWeek.get_previous_term({'year': 2021,
                                                    'quarter': 'autumn'}),
                         {'year': 2021, 'quarter': 'summer'})
        self.assertEqual(RADWeek.get_previous_term({'year': 2021,
                                                    'quarter': 'winter'}),
                         {'year': 2020, 'quarter': 'autumn'})

    def test_signins(self):
        signins = CourseAnalyticsScores.get_signins_by_netid('javerage')
        print(signins)
        self.assertEqual(len(signins), 3)
