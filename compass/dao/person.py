# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_pws import PWS, InvalidNetID, DataFailureException
import re

system_key_re = re.compile(r'^\d{9}$')


def valid_uwnetid(s):
    return PWS().valid_uwnetid(s)


def valid_uwregid(s):
    return PWS().valid_uwregid(s)


def valid_student_number(s):
    return PWS().valid_student_number(s)


def valid_system_key(s):
    return (s is not None and system_key_re.match(str(s)) is not None)


def is_overridable_uwnetid(username):
    error_msg = "No override user supplied, please enter a UWNetID"
    if username is not None and len(username) > 0:
        try:
            person = PWS().get_person_by_netid(username)
            if username.lower() == person.uwnetid:
                error_msg = None
            else:
                error_msg = "Current UWNetID: {}, Prior UWNetID: ".format(
                    person.uwnetid)
        except InvalidNetID:
            error_msg = "Not a valid UWNetID: "
        except DataFailureException as err:
            if err.status == 404:
                error_msg = 'UWNetID not found: '
            else:
                error_msg = "Error ({}) {}: ".format(err.status, err.msg)
    return error_msg
