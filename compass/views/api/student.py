# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.dao.photo import PhotoDAO
from compass.models import (
    Student, Contact, StudentAffiliation, Visit, StudentEligibility)
from compass.serializers import (
    ContactReadSerializer, StudentAffiliationReadSerializer,
    VisitReadSerializer, StudentWriteSerializer,
    StudentEligibilityReadSerializer)
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseNotFound
from restclients_core.exceptions import DataFailureException
from rest_framework.response import Response
from rest_framework import status
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
from uw_sws.term import (
    get_current_term, get_next_term, get_term_after,
    get_term_by_year_and_quarter)
from uw_sws.registration import get_schedule_by_regid_and_term
from uw_sws.enrollment import get_enrollment_history_by_regid

TERMS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Autumn"}


class StudentView(BaseAPIView):
    '''
    API endpoint returning a student's details

    /api/internal/student/[student_number|uwnetid]/
    '''
    def get(self, request, student_identifier):
        access_groups = self.get_access_groups(request)
        try:
            client = UWPersonClient()
            try:
                person = client.get_person_by_uwnetid(student_identifier)
            except PersonNotFoundException:
                person = client.get_person_by_student_number(
                    student_identifier)
            person.photo_url = PhotoDAO().get_photo_url(person.uwregid)
            return JsonResponse(person.to_dict(), safe=False)
        except PersonNotFoundException:
            return HttpResponseNotFound()

    def post(self, request, student_identifier=None):
        access_groups = self.get_access_groups(request)
        try:
            # check user permissions for every group that the user belongs to
            for group in access_groups:
                self.validate_user_access(request, group.id)
            data = request.data
            system_key = data.get("system_key")
            student_record = {}
            student_record['system_key'] = system_key
            student_record['programs'] = data.get('programs')
            try:
                # update existing student record if one exists
                student, _ = Student.objects.get_or_create(
                    system_key=system_key)
                serializer = StudentWriteSerializer(student,
                                                    data=student_record)
            except Student.DoesNotExist:
                # create new student record
                serializer = StudentWriteSerializer(data=student_record)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response("User not authorized to update student data.",
                            status=status.HTTP_401_UNAUTHORIZED)


class StudentSchedulesView(BaseAPIView):
    '''
    API endpoint returning a student's class schedule details

    /api/internal/student/[uwregid]/schedules/
    '''
    def get(self, request, uwregid):
        cur_term = get_current_term()
        next_term = get_next_term()
        term_after = get_term_after(next_term)
        terms = [cur_term, next_term, term_after]
        schedules = {}
        for index, term in enumerate(terms):
            try:
                schedules[index] = \
                    get_schedule_by_regid_and_term(uwregid, term).json_data()
            except DataFailureException:
                continue
        return JsonResponse(schedules, safe=False)


class StudentContactsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/student/[systemkey]/contacts/
    '''

    def get(self, request, systemkey):
        queryset = Contact.objects.filter(
            student__system_key=systemkey).order_by('-checkin_date')
        serializer = ContactReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentAffiliationsView(BaseAPIView):
    '''
    API endpoint returning a list of affiliations for a student

    /api/internal/student/[systemkey]/affiliations/
    '''

    def get(self, request, systemkey):
        access_groups = self.get_access_groups(request)
        affiliations = []

        try:
            student_affiliations = StudentAffiliation.objects.filter(
                student__system_key=systemkey,
                affiliation__access_group__in=access_groups)

            for sa in student_affiliations:
                affiliations.append(
                    StudentAffiliationReadSerializer(sa).data)
        except StudentAffiliation.DoesNotExist:
            pass

        return Response(affiliations, status=status.HTTP_200_OK)


class StudentVisitsView(BaseAPIView):
    '''
    API endpoint returning a list of visits for a student

    /api/internal/student/[systemkey]/visits/
    '''
    def get(self, request, systemkey):
        access_groups = self.get_access_groups(request)
        queryset = Visit.objects.filter(
            student__system_key=systemkey,
            visit_type__access_group__in=access_groups).order_by(
                '-checkin_date')
        serializer = VisitReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentTranscriptsView(BaseAPIView):
    '''
    API endpoint returning a list of transcripts for a student

    /api/internal/student/[uwregid]/transcripts/
    '''
    def get(self, request, uwregid):
        client = UWPersonClient()
        person = client.get_person_by_uwregid(uwregid)

        transcripts = []
        for transcript in sorted(person.student.transcripts, key=lambda t: (
                t.tran_term.year, t.tran_term.quarter), reverse=True):
            term = get_term_by_year_and_quarter(
                transcript.tran_term.year,
                TERMS[transcript.tran_term.quarter])
            try:
                class_schedule = get_schedule_by_regid_and_term(
                    uwregid, term)
                transcript.class_schedule = class_schedule.json_data()
            except DataFailureException:
                transcript.class_schedule = None
            transcripts.append(transcript.to_dict())

        return JsonResponse(transcripts, safe=False)


class StudentEligibilityView(BaseAPIView):
    '''
    API endpoint returning a list of eligible resources for a student

    /api/internal/student/[systemkey]/eligibility[/eligibility_id]
    '''
    def get(self, request, systemkey, eligibility_id):
        access_groups = self.get_access_groups(request)
        queryset = StudentEligibility.objects.filter(
            student__system_key=systemkey,
            eligibility_type__access_group__in=access_groups)
        serializer = StudentEligibilityReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
