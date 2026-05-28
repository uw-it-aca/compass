# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from uw_compass_visits import CompassVisits
from uw_compass_visits.models import Visit
from restclients_core.exceptions import DataFailureException
from compass.models import AccessGroup


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
    except DataFailureException as ex:
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
        for visit in visits['pending_verification']:
            visit_resp['pending_verification'].append(visit.json_data())
        for visit in visits['pending_checkout']:
            if visit.program_area not in visit_resp['by_programarea']:
                visit_resp['by_programarea'][visit.program_area] = []
                visit_resp['by_programarea'][visit.program_area].append(
                    visit.json_data())
            else:
                visit_resp['by_programarea'][visit.program_area].append(
                    visit.json_data())

    except DataFailureException as ex:
        # If there are no visits, return an empty response
        pass
    return visit_resp


def get_visit_options(uwregid):
    """
    Returns a list of visit options for the given UW regid.
    """
    options = []
    try:
        options = CompassVisits().get_visit_options(uwregid)
    except DataFailureException as ex:
        # If there are no visit options, return an empty list
        options = []
    return options


def admin_create_visit(visit_data):
    """
    Creates a visit with the given visit data.
    """
    visit = Visit(
        access_group=get_compass_visits_access_group(),
        student_syskey=visit_data.get('student_syskey'),
        program_area=visit_data.get('program_area'),
        tutoring_option=visit_data.get('tutoring_option'),
        writing_service=visit_data.get('writing_service'),
        course=visit_data.get('course'),
    )
    return CompassVisits().admin_create_visit(visit)


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
