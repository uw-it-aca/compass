# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import random
from django.db import IntegrityError
from compass.tests import CompassTestCase
from compass.models.rad_data import (RADWeek, RADImport, CourseAnalyticsScores,
                                     StudentAlertStatus,
                                     convert_score_range)


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
                                 import_status=RADImport.SUCCESS)

        year, quarter, week = RADImport.get_next_import_week()
        self.assertEqual(year, 2021)
        self.assertEqual(quarter, 'summer')
        self.assertEqual(week, 1)
        RADImport.objects.create(week=w2,
                                 import_status=RADImport.SUCCESS)
        year, quarter, week = RADImport.get_next_import_week()
        self.assertEqual(year, 2022)
        self.assertEqual(quarter, 'winter')
        self.assertEqual(week, 1)

    def test_get_recent_week(self):
        w2 = RADWeek.get_or_create_week(year=2021,
                                        quarter='autumn',
                                        week=9)
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


class RADImportTest(CompassTestCase):
    RAD_WEEK = None

    def setUp(self):
        self.RAD_WEEK = RADWeek.get_or_create_week(year=2021,
                                                   quarter='spring',
                                                   week=10)

    def test_get_filename(self):
        rad_import = RADImport.objects.create(week=self.RAD_WEEK,
                                              import_status=RADImport.SUCCESS)
        self.assertEqual(rad_import.get_filename(),
                         '2021-spring-week-10-compass-data.csv')

    def test_next_import_week_first_import(self):
        with self.assertRaises(RADImport.DoesNotExist):
            RADImport.get_next_import_week()

    def test_next_import_week(self):
        start_week = RADWeek.get_or_create_week(year=2021,
                                                quarter='spring',
                                                week=1)
        RADImport.objects.create(week=start_week,
                                 import_status=RADImport.SUCCESS)
        next_year, next_quarter, next_week = RADImport.get_next_import_week()
        self.assertEqual(next_year, 2021)
        self.assertEqual(next_quarter, 'spring')
        self.assertEqual(next_week, 2)

    def test_next_import_week_qtr_turn(self):
        RADImport.objects.create(week=self.RAD_WEEK,
                                 import_status=RADImport.SUCCESS)
        next_year, next_quarter, next_week = RADImport.get_next_import_week()
        self.assertEqual(next_year, 2021)
        self.assertEqual(next_quarter, 'summer')
        self.assertEqual(next_week, 1)

    def test_next_import_yr_turn(self):
        last_week_in_yr = RADWeek.get_or_create_week(year=2021,
                                                     quarter='autumn',
                                                     week=10)
        RADImport.objects.create(week=last_week_in_yr,
                                 import_status=RADImport.SUCCESS)
        next_year, next_quarter, next_week = RADImport.get_next_import_week()
        self.assertEqual(next_year, 2022)
        self.assertEqual(next_quarter, 'winter')
        self.assertEqual(next_week, 1)

    def test_create_job(self):
        week = RADWeek.get_or_create_week(year=2021,
                                          quarter='spring',
                                          week=10)

        rad_import = RADImport.create_job(week)
        self.assertEqual(rad_import.week.year, 2021)
        with self.assertRaises(ValueError):
            RADImport.create_job(week)
        RADImport.create_job(week, reload=True)


class CourseAnalyticsScoresTest(CompassTestCase):
    RAD_WEEK = None

    def setUp(self):
        self.RAD_WEEK = RADWeek.get_or_create_week(year=2021,
                                                   quarter='spring',
                                                   week=5)

    def test_json_data(self):
        score = CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 A",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=0
        )
        json_data = score.json_data()
        self.assertEqual(json_data['activity_score'], 90.0)
        self.assertEqual(json_data['assignment_score'], 100)
        self.assertEqual(json_data['grade_score'], 80)
        self.assertEqual(json_data['prediction_score'], 0)
        self.assertEqual(json_data['week_id'], 5)

    def test_convert_score_range(self):
        self.assertEqual(convert_score_range(-5), 0)
        self.assertEqual(convert_score_range(-4.5), 5.0)
        self.assertEqual(convert_score_range(0), 50)
        self.assertEqual(convert_score_range(5), 100)

    def test_alert_status(self):
        score = CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 A",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=5,
            prediction_score=0
        )
        self.assertFalse(score.is_alert_status())
        score.delete()

        score_alert = CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 A",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=2,
            prediction_score=1
        )
        self.assertTrue(score_alert.is_alert_status())

    def test_get_rad_data_for_course(self):
        CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 A",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=0
        )
        data = CourseAnalyticsScores.get_rad_data_for_course(2021,
                                                             'spring',
                                                             'javerage',
                                                             'CSE 142 A')
        self.assertEqual(len(data), 1)

    def test_get_all_pred_for_week(self):
        CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 A",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=0
        )
        CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 B",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=1
        ),
        CourseAnalyticsScores.objects.create(
            uwnetid="jbelowaverage",
            course="CSE 144 B",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=1
        )
        CourseAnalyticsScores.objects.create(
            uwnetid="jbelowaverage",
            course="CSE 145 B",
            week=self.RAD_WEEK,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=1
        )

        data = CourseAnalyticsScores.get_all_predections_for_week(
            self.RAD_WEEK)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['javerage'], [0, 1])
        self.assertEqual(data['jbelowaverage'], [1, 1])


class StudentAlertStatusTest(CompassTestCase):
    RAD_WEEK = None

    def setUp(self):
        self.RAD_WEEK = RADWeek.get_or_create_week(year=2021,
                                                   quarter='spring',
                                                   week=5)

    def test_alert_status(self):
        self.assertEqual(StudentAlertStatus.get_alert_class_from_scores([]),
                         None)
        self.assertEqual(StudentAlertStatus.get_alert_class_from_scores([0]),
                         StudentAlertStatus.AlertStatus.SUCCESS)
        self.assertEqual(StudentAlertStatus.get_alert_class_from_scores([1]),
                         StudentAlertStatus.AlertStatus.DANGER)
        self.assertEqual(StudentAlertStatus.get_alert_class_from_scores(
            [0, 0, 1]),
            StudentAlertStatus.AlertStatus.WARNING)
        self.assertEqual(StudentAlertStatus.get_alert_class_from_scores(
            [1, None, None]),
            StudentAlertStatus.AlertStatus.DANGER)

    def test_alert_class(self):
        StudentAlertStatus.objects.create(
            uwnetid="javerage",
            alert_status=StudentAlertStatus.AlertStatus.SUCCESS
        )
        alert = StudentAlertStatus.objects.get(uwnetid="javerage")
        self.assertEqual(alert.get_alert_status_display(), 'success')

    def test_get_by_week_uwnetid(self):
        StudentAlertStatus.objects.create(
            uwnetid="javerage",
            alert_status=StudentAlertStatus.AlertStatus.DANGER
        )
        alert_class = \
            StudentAlertStatus.get_alert_class_by_uwnetid("javerage")
        self.assertEqual(alert_class,
                         "danger")

    def test_constraints(self):
        StudentAlertStatus.objects.create(
            uwnetid="javerage",
            alert_status=StudentAlertStatus.AlertStatus.SUCCESS
        )
        with self.assertRaises(IntegrityError):
            StudentAlertStatus.objects.create(
                uwnetid="javerage",
                alert_status=StudentAlertStatus.AlertStatus.SUCCESS
            )
