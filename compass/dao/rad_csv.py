# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
from io import StringIO
from logging import getLogger

from compass.models.rad_data import CourseAnalyticsScores, StudentSigninAnalytics

logger = getLogger(__name__)

BULK_CREATE_BUCKET_SIZE = 1000


def read_csv(csv_string):
    """
    Yield each row from a CSV string as a dictionary.
    """
    reader = csv.DictReader(StringIO(csv_string))
    yield from reader


def update_prediction_scores(week, pred_file):
    """
    Update only prediction_score for existing CourseAnalyticsScores rows
    for the given week without re-importing canvas analytics data.
    """
    pred_dict = _get_prediction_dict(pred_file)
    rows = list(CourseAnalyticsScores.objects.filter(week=week))
    for row in rows:
        row.prediction_score = pred_dict.get(
            f"{row.uwnetid}_{row.course}", None)
    updated = 0
    for i in range(0, len(rows), BULK_CREATE_BUCKET_SIZE):
        batch = rows[i:i + BULK_CREATE_BUCKET_SIZE]
        CourseAnalyticsScores.objects.bulk_update(batch, ['prediction_score'])
        updated += len(batch)
    logger.info(
        f"Updated prediction scores for {updated} rows in week {week}")


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
    Get prediction data for a given term, grouped by user and course_id.
    """
    prediction_dict = {}
    for row in read_csv(pred_file):
        key = f"{row['uw_netid'].strip()}_{row['course_code'].strip()}"
        pred_value = row['pred'].strip()
        if pred_value in {"True", "False"}:
            prediction_dict[key] = 1.0 if pred_value == "True" else 0.0
        else:
            raise ValueError(f"Invalid prediction value '{pred_value}'"
                             f" for key '{key}'")
    return prediction_dict


def validate_prediction_json(pred_json):
    """
    Validate prediction JSON structure.
    """
    required_fields = {'uw_netid', 'course_code', 'pred'}
    rows = pred_json.get('body', [])
    if not rows:
        raise ValueError("Prediction JSON body is empty")
    for row in rows:
        missing = required_fields - row.keys()
        if missing:
            raise ValueError(f"Missing fields in prediction JSON:"
                             f" {', '.join(missing)}")


def get_pred_csv_from_json(pred_json):
    """
    Convert prediction JSON to CSV string.
    """
    output = StringIO()
    writer = csv.DictWriter(output,
                            fieldnames=['uw_netid',
                                        'course_code',
                                        'pred'])
    writer.writeheader()
    for row in pred_json.get('body', []):
        writer.writerow({
            'uw_netid': row['uw_netid'],
            'course_code': row['course_code'],
            'pred': row['pred']
        })
    return output.getvalue()


def _parse_score(field):
    return 0 if not field else float(field)
