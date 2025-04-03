# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models import CharField, OuterRef, Subquery, Value, F
from django.db.models.functions import JSONObject, Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.conf import settings
from django.core.cache import cache
from uw_person_client.models import (
    Person, Adviser, Student, Transcript, Degree)
from uw_person_client.exceptions import (
    PersonNotFoundException, AdviserNotFoundException)
from uw_pws import PWS, InvalidNetID, DataFailureException
from compass.dao.photo import PhotoDAO
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


def get_transcripts_by_uwregid(uwregid):
    person = get_person_by_uwregid(
        uwregid, include_student=True, include_student_transcripts=True)

    if person.student is not None and person.student.transcripts is not None:
        return person.student.transcripts.all()
    return []


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


def get_students_by_system_keys(system_keys, **kwargs):
    photo_key = PhotoDAO().generate_photo_key()
    students = Student.objects.filter(
            system_key__in=system_keys
        ).values(
            'system_key',
            'student_number',
            'person__uwnetid',
            'person__uwregid',
            'person__pronouns',
            'person__display_name',
            'person__first_name',
            'person__surname',
        ).annotate(
            uwnetid=F('person__uwnetid'),
            pronouns=F('person__pronouns'),
            display_name=F('person__display_name'),
            first_name=F('person__first_name'),
            surname=F('person__surname'),
            photo_url=Concat(
                Value('/api/internal/photo/'), F('person__uwregid'),
                Value(f'/{photo_key}/'), output_field=CharField()),
            adviser_uwnetids=ArrayAgg('advisers__employee__person__uwnetid')
        )

    students_dict = {}
    for student in students:
        students_dict[student['system_key']] = student
    return students_dict


def get_students_by_student_numbers(student_numbers, **kwargs):
    students = Student.objects.filter(
            student_number__in=student_numbers
        ).values(
            'system_key',
            'student_number',
            'person__uwnetid',
            'person__uwregid',
            'person__pronouns',
            'person__display_name',
            'person__first_name',
            'person__surname',
        ).annotate(
            uwnetid=F('person__uwnetid'),
            pronouns=F('person__pronouns'),
            display_name=F('person__display_name'),
            first_name=F('person__first_name'),
            surname=F('person__surname')
        )

    students_dict = {}
    for student in students:
        students_dict[student['student_number']] = student
    return students_dict


def get_adviser_caseload(uwnetid):
    adviser = Adviser.objects.get_adviser_by_uwnetid(uwnetid)
    photo_key = PhotoDAO().generate_photo_key()

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
                ).order_by('-degree_index')[:1])
        ).filter(advisers__in=[adviser]).values(
            'student_number',
            'class_desc',
            'academic_term__year',
            'academic_term__quarter',
            'registered_in_quarter',
            'registration_hold_ind',
            'campus_desc',
            'special_program_code',
            'special_program_desc',
            'enroll_status_code',
            'person__uwnetid',
            'person__uwregid',
            'person__pronouns',
            'person__display_name',
            'latest_transcript',
            'latest_degree'
        ).annotate(
            uwnetid=F('person__uwnetid'),
            uwregid=F('person__uwregid'),
            pronouns=F('person__pronouns'),
            display_name=F('person__display_name'),
            photo_url=Concat(
                Value('/api/internal/photo/'), F('person__uwregid'),
                Value(f'/{photo_key}/'), output_field=CharField())
        ).order_by('person__surname', 'person__first_name')
