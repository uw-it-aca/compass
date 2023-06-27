# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_pws import PWS, InvalidNetID
from compass.clients import CompassPersonClient, PersonNotFoundException
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


def person_from_uwnetid(uwnetid):
    if not valid_uwnetid(uwnetid):
        raise InvalidNetID
    return CompassPersonClient().get_person_by_uwnetid(uwnetid)


def is_overridable_uwnetid(username):
    error_msg = "No override user supplied, please enter a UWNetID"
    if username is not None and len(username) > 0:
        try:
            person = person_from_uwnetid(username.lower())
            if username.lower() != person.uwnetid:
                error_msg = f"Current netid: {person.uwnetid}, Prior netid: "
        except InvalidNetID:
            error_msg = "Not a valid UWNetID: "
        except PersonNotFoundException:
            error_msg = "UWNetID not found: "
    return error_msg
