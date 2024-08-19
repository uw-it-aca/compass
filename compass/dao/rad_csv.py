# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import csv
from io import StringIO
from compass.models.rad_data import RADDataPoint


def read_csv(csv_string):
    """
    Read CSV string and return list of dictionaries.
    """
    reader = csv.DictReader(StringIO(csv_string))
    return list(reader)


def import_data_from_csv(week, csv_string):
    """
    Import data from CSV string into RADImport model.
    """
    data = read_csv(csv_string)
    for row in data:
        RADDataPoint.objects.create(uwnetid=row['uw_netid'],
                                    week=week,
                                    course=row['course_code'],
                                    activity_score=row['activity'],
                                    assignment_score=row['assignments'],
                                    grade_score=row['grades'],
                                    prediction_score=row['pred'],
                                    signin_score=row['sign_in'])
