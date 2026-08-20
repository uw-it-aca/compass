# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from restclients_core.exceptions import DataFailureException
from uw_compass_visits import CompassVisits
from uw_compass_visits.models import Visit

from compass.dao.person import get_students_by_system_keys
from compass.models import AccessGroup, VisitTutoringOption, VisitType

"""
This module provides functions for interacting with the Compass Visits
application via the CompassVisits restclient.
"""


def get_visits_for_student(netid):
    # TODO: Switch to syskey
    """
    Returns a list of visits for the given student netid.
    """
    visits = None
    try:
        visits = CompassVisits().get_visits_for_student(netid)
    except DataFailureException:
        # If the student doesn't have any visits, return an empty list
        visits = []
    return visits


def get_admin_visit_list():
    """
    Returns a list of all visits for admin users.
    """
    visit_resp = {
        'pending_verification': [],
        'by_programarea': {},
    }
    try:
        visits = CompassVisits().get_visit_admin_list()
        access_group = get_compass_visits_access_group()
        program_area_names = dict(
            VisitType.objects.filter(
                access_group=access_group,
                is_compass_visits_program_area=True,
            ).values_list('slug', 'name')
        )
        tutoring_option_names = dict(
            VisitTutoringOption.objects.filter(
                access_group=access_group
            ).values_list('slug', 'name')
        )
        student_syskeys = [visit.student_syskey for visit in
                           visits['pending_verification']]
        student_syskeys += [visit.student_syskey for visit in
                            visits['pending_checkout']]
        student_syskeys = list(set(student_syskeys))
        students_dict = get_students_by_system_keys(student_syskeys)

        for visit in visits['pending_verification']:
            student = students_dict.get(visit.student_syskey)
            visit_json = visit.json_data()
            visit_json['program_area'] = program_area_names.get(
                visit.program_area, visit.program_area)
            visit_json['tutoring_option'] = tutoring_option_names.get(
                visit.tutoring_option, visit.tutoring_option)
            visit_json['student'] = student if student else None
            visit_resp['pending_verification'].append(visit_json)
        for visit in visits['pending_checkout']:
            visit_json = visit.json_data()
            program_area = program_area_names.get(
                visit.program_area, visit.program_area)
            visit_json['program_area'] = program_area
            visit_json['tutoring_option'] = tutoring_option_names.get(
                visit.tutoring_option, visit.tutoring_option)
            student = students_dict.get(visit.student_syskey)
            visit_json['student'] = student if student else None
            visit_resp['by_programarea'].setdefault(
                program_area, []).append(visit_json)

    except DataFailureException:
        # If there are no visits, return an empty response
        pass
    return visit_resp


def get_visit_options(uwregid):
    """
    Returns visit options for the given UW regid.
    """
    options = {
        'program_areas': [],
        'tutoring_options': [],
        'writing_services': [],
        'courses': [],
    }
    try:
        options = CompassVisits().get_visit_options(uwregid)
    except DataFailureException:
        # If there are no visit options, return an empty options payload.
        pass
    return options


def admin_create_visit(visit_data):
    """
    Creates a visit with the given visit data.  Automatically verify as it is
    created by an admin user.
    """
    student_syskey = visit_data.get('student_syskey')
    if student_syskey and _student_has_active_visit(student_syskey):
        raise DataFailureException(
            'compass-visits',
            400,
            'Student already has an active visit')

    visit = Visit(
        access_group=get_compass_visits_access_group(),
        student_syskey=student_syskey,
        program_area=visit_data.get('program_area'),
        tutoring_option=visit_data.get('tutoring_option'),
        writing_service=visit_data.get('writing_service'),
        course=visit_data.get('course'),
        is_verified=True,
    )
    return CompassVisits().admin_create_visit(visit)


def _student_has_active_visit(student_syskey):
    """
    Returns True when the student appears in pending verification or
    pending checkout visit lists.
    """
    try:
        visits = CompassVisits().get_visit_admin_list()
    except DataFailureException:
        return False

    pending_verification = visits.get('pending_verification', [])
    pending_checkout = visits.get('pending_checkout', [])
    for visit in pending_verification + pending_checkout:
        if visit.student_syskey == student_syskey:
            return True
    return False


def admin_update_visit(visit_id, is_verified=False, is_checked_out=False):
    """
    Updates a visit with the given visit data.
    """
    return CompassVisits().admin_update_visit(visit_id,
                                              verify=is_verified,
                                              checkout=is_checked_out)


def admin_delete_visit(visit_id):
    """
    Deletes a visit with the given visit id.
    """
    return CompassVisits().admin_delete_visit(visit_id)


def get_compass_visits_access_group():
    """
    Returns the AccessGroup object for Compass Visits.  Currently only
    OMAD has access to Compass Visits.
    """
    try:
        access_group_name = settings.COMPASS_VISITS_ACCESS_GROUP_NAME
    except AttributeError:
        raise ImproperlyConfigured(
            "COMPASS_VISITS_ACCESS_GROUP_NAME is not configured in settings."
        )
    try:
        return AccessGroup.objects.get(name=access_group_name)
    except AccessGroup.DoesNotExist:
        raise ImproperlyConfigured(
            f"Access group matching "
            f"'{access_group_name}' not found. "
        )
