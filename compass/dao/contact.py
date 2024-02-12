# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from compass.models import ContactType, AccessGroup, AppUser
from dateutil import parser


def validate_contact_post_data(contact_dict):
    access_group = AccessGroup.objects.by_name("OMAD")
    # check that adviser netid is defined
    validate_adviser_netid(contact_dict.get("adviser_netid"))
    # check that system key is defined
    validate_student_systemkey(
        contact_dict.get("student_systemkey"))
    # parse checkin date to ensure it is in the correct format
    contact_dict["checkin_date"] = parse_checkin_date_str(
        contact_dict.get("checkin_date"))
    # verify that the specified contact type exists in OMAD
    contact_dict["contact_type"] = parse_contact_type_str(
        contact_dict.get("contact_type"), access_group)

    # if the adviser is a member of the omad group and the contact record
    # was successfully parsed, create an app-user and a student record for
    # them if one doesn't already exist
    app_user = AppUser.objects.upsert_appuser(
        contact_dict["adviser_netid"])


def validate_adviser_netid(adviser_netid):
    if adviser_netid is None:
        raise ValueError("Missing adviser netid")


def validate_student_systemkey(student_systemkey):
    if student_systemkey is None:
        raise ValueError("Missing student systemkey")

    try:
        if not student_systemkey.isdigit():
            raise ValueError("Student systemkey is not a positive integer")
    except AttributeError as e:
        raise ValueError(f"Invalid student systemkey: {e}")


def pad_student_systemkey(student_systemkey):
    return student_systemkey.zfill(9)


def parse_checkin_date_str(checkin_date_str):
    # parse checkin date
    if checkin_date_str is None:
        raise ValueError("Check-in date not specified")
    else:
        try:
            dt = parser.parse(checkin_date_str,
                              tzinfos=getattr(settings, "TZINFOS", {}))
            if dt.tzinfo is None:
                raise ValueError("Invalid check-in date, missing timezone")
            return dt
        except parser.ParserError as e:
            raise ValueError(f"Invalid check-in date: {e}")


def parse_contact_type_str(contact_type_str, access_group):
    try:
        return ContactType.objects.get(access_group=access_group,
                                       slug=contact_type_str)
    except ContactType.DoesNotExist:
        raise ValueError(
            f"Contact type '{contact_type_str}' does not exist "
            f"for the {access_group.name} access group.")
