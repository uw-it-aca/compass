# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_compass_visits import CompassVisits
from restclients_core.exceptions import DataFailureException


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
        for visit in visits:
            if not visit.is_verified:
                visit_resp['pending_verification'].append(visit.json_data())
            else:
                if visit.program_area not in visit_resp['by_programarea']:
                    visit_resp['by_programarea'][visit.program_area] = []
                visit_resp['by_programarea'][visit.program_area].append(
                    visit.json_data())

    except DataFailureException as ex:
        # If there are no visits, return an empty response
        pass
    return visit_resp


def get_visit_options():
    """
    Returns a list of visit options.
    """
    options = []
    try:
        options = CompassVisits().get_visit_options()
    except DataFailureException as ex:
        # If there are no visit options, return an empty list
        options = []
    return options


def admin_create_visit(visit_data):
    """
    Creates a visit with the given visit data.
    """
    return CompassVisits().admin_create_visit(visit_data)


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
