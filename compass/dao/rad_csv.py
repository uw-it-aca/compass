# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import csv
from io import StringIO
from compass.models.rad_data import (CourseAnalyticsScores,
                                     StudentSigninAnalytics)


def read_csv(csv_string):
    """
    Read CSV string and return list of dictionaries.
    """
    reader = csv.DictReader(StringIO(csv_string))
    return list(reader)


def import_data_from_csv(week, csv_string, reload=False):
    """
    Import data from CSV string into RADImport model.
    """
    data = read_csv(csv_string)
    processed_netids = []
    if reload:
        StudentSigninAnalytics.objects.filter(week=week).delete()
        CourseAnalyticsScores.objects.filter(week=week).delete()
    for row in data:
        if row['uw_netid'] not in processed_netids:
            StudentSigninAnalytics.objects.create(uwnetid=row['uw_netid'],
                                                  week=week,
                                                  signin_score=row['sign_in'])
            processed_netids.append(row['uw_netid'])
        CourseAnalyticsScores.objects.create(uwnetid=row['uw_netid'],
                                             week=week,
                                             course=row['course_code'],
                                             activity_score=row['activity'],
                                             assignment_score=row['assignments'],
                                             grade_score=row['grades'],
                                             prediction_score=row['pred'])
