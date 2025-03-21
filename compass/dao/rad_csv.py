# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
from io import StringIO
from compass.models.rad_data import (CourseAnalyticsScores,
                                     StudentSigninAnalytics)
from django.db import IntegrityError
from logging import getLogger

from compass.views.api.student import StudentSigninAnalyticsView

logger = getLogger(__name__)

BULK_CREATE_BUCKET_SIZE = 1000


def read_csv(csv_string):
    """
    Read CSV string and return list of dictionaries.
    """
    reader = csv.DictReader(StringIO(csv_string))
    return list(reader)


def import_data_from_csv(week, csv_string, pred_file, reload=False):
    """
    Import data from CSV string into RADImport model.
    """
    data = read_csv(csv_string)
    processed_netids = {}
    processed_per_netid_courses = {}

    if pred_file is None:
        pred_dict = {}
    else:
        pred_dict = _get_prediction_dict(pred_file)

    if reload:
        StudentSigninAnalytics.objects.filter(week=week).delete()
        CourseAnalyticsScores.objects.filter(week=week).delete()

    course_analytics_scores = []
    student_signin_analytics = []
    i = 0
    for row in data:
        if row['uw_netid'] not in processed_netids:
            student_signin_analytics.append(
                StudentSigninAnalytics(uwnetid=row['uw_netid'],
                                       week=week,
                                       signin_score=_parse_score(
                                           row['sign_in'])
                                       )
            )
            processed_netids[row['uw_netid']] = True
        # Catch dupes manually so we can use more performant bulk_create
        per_netid_course_str = f"{row['uw_netid']}_{row['course_code']}"
        if per_netid_course_str not in processed_per_netid_courses:
            pred_score = pred_dict.get(per_netid_course_str, None)
            course_analytics_scores.append(
                CourseAnalyticsScores(
                    uwnetid=row['uw_netid'],
                    week=week,
                    course=row['course_code'],
                    activity_score=_parse_score(row['activity']),
                    assignment_score=_parse_score(row['assignments']),
                    grade_score=_parse_score(row['grades']),
                    prediction_score=pred_score))
            processed_per_netid_courses[per_netid_course_str] = True
        else:
            logger.error(f"Duplicate analytics found for {row['uw_netid']}, "
                         f"{row['course_code']}")
            continue
        i += 1
        if i == BULK_CREATE_BUCKET_SIZE:
            StudentSigninAnalytics.objects.bulk_create(
                student_signin_analytics)
            CourseAnalyticsScores.objects.bulk_create(
                course_analytics_scores)
            i = 0
            student_signin_analytics = []
            course_analytics_scores = []
    StudentSigninAnalytics.objects.bulk_create(student_signin_analytics)
    CourseAnalyticsScores.objects.bulk_create(course_analytics_scores)


def _get_prediction_dict(pred_file):
    """
    Get prediction data for a given term. grouped by user and course_id
    """

    prediction_data = read_csv(pred_file)
    prediction_dict = {}
    for row in prediction_data:
        key = f"{row['uw_netid'].strip()}_{row['course_code'].strip()}"
        prediction_dict[key] = row['pred']
    return prediction_dict


def _parse_score(field):
    return 0 if not field else float(field)
