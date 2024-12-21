# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management import call_command
from compass.tests import CompassTestCase
from compass.models.rad_data import (RADWeek,
                                     StudentAlertStatus,
                                     CourseAnalyticsScores)


class TestGenerateAlertStatus(CompassTestCase):

    def setUp(self):
        rad_week = RADWeek.get_or_create_week(year=2021,
                                              quarter='spring',
                                              week=10)
        CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 A",
            week=rad_week,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=0
        )
        CourseAnalyticsScores.objects.create(
            uwnetid="javerage",
            course="CSE 142 B",
            week=rad_week,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=1
        ),
        CourseAnalyticsScores.objects.create(
            uwnetid="jbelowaverage",
            course="CSE 144 B",
            week=rad_week,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=1
        )
        CourseAnalyticsScores.objects.create(
            uwnetid="jbelowaverage",
            course="CSE 145 B",
            week=rad_week,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=1
        )
        CourseAnalyticsScores.objects.create(
            uwnetid="jaboveaverage",
            course="CSE 145 B",
            week=rad_week,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=0
        )
        CourseAnalyticsScores.objects.create(
            uwnetid="junknown",
            course="CSE 145 B",
            week=rad_week,
            activity_score=4,
            assignment_score=5,
            grade_score=3,
            prediction_score=None
        )
        pass

    def test_gen(self):
        call_command('generate_alert_status')
        alert_status = StudentAlertStatus.objects.all()
        self.assertEqual(len(alert_status), 4)
