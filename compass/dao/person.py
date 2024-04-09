# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import JSONObject
from django.conf import settings
from django.core.cache import cache
from uw_person_client.models import (
    Person, Adviser, Student, Transcript, Degree)
from uw_person_client.exceptions import (
    PersonNotFoundException, AdviserNotFoundException)
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


def get_person_by_uwnetid(uwnetid, **kwargs):
    return Person.objects.get_person_by_uwnetid(uwnetid, **kwargs)


def get_person_by_uwregid(uwregid, **kwargs):
    return Person.objects.get_person_by_uwregid(uwregid, **kwargs)


def get_person_by_system_key(system_key, **kwargs):
    return Person.objects.get_person_by_system_key(system_key, **kwargs)


def get_person_by_student_number(student_number, **kwargs):
    return Person.objects.get_person_by_student_number(
        student_number, **kwargs)


def get_appuser_by_uwnetid(uwnetid):
    """
    Returns a cached person model for use with AppUser.
    """
    cache_key = f'appuser_{uwnetid}'

    person_data = cache.get(cache_key)
    if person_data is not None:
        return Person(**person_data)

    person = get_person_by_uwnetid(uwnetid)

    cache.set(
        cache_key,
        person.to_dict(),
        timeout=getattr(settings, 'APPUSER_PERSON_EXPIRES', 60 * 60 * 24)
    )
    return person


def get_adviser_caseload(uwnetid):
    adviser = Adviser.objects.get_adviser_by_uwnetid(uwnetid)

    return Student.objects.annotate(latest_transcript=Subquery(
            Transcript.objects.filter(
                student=OuterRef('pk')).values(json=JSONObject(
                    scholarship_type='scholarship_type',
                    scholarship_desc='scholarship_desc')
                ).order_by('-tran_term__year', '-tran_term__quarter')[:1])
        ).annotate(latest_degree=Subquery(
            Degree.objects.filter(
                student=OuterRef('pk')).values(json=JSONObject(
                    degree_status_desc='degree_status_desc')
                ).order_by('-degree_date')[:1])
        ).filter(advisers__in=[adviser]).values(
            'student_number',
            'gender',
            'class_desc',
            'academic_term__year',
            'academic_term__quarter',
            'registered_in_quarter',
            'registration_hold_ind',
            'campus_desc',
            'special_program_code',
            'special_program_desc',
            'enroll_status_code',
            'enroll_status_request_code',
            'enroll_status_desc',
            'person__display_name',
            'person__uwnetid',
            'person__uwregid',
            'person__pronouns',
            'person__surname',
            'latest_transcript',
            'latest_degree'
        ).annotate(
            display_name=F('person__display_name'),
            uwnetid=F('person__uwnetid'),
            uwregid=F('person__uwregid'),
            pronouns=F('person__pronouns'),
            surname=F('person__surname')
        ).order_by('person__surname')
