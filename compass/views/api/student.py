# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.dao.photo import PhotoDAO
from compass.dao.person import (
    valid_uwnetid, valid_uwregid, valid_student_number, valid_system_key)
from compass.models import (
    Student, Contact, StudentAffiliation, Affiliation, Cohort,
    Visit, EligibilityType, StudentEligibility)
from compass.serializers import (
    ContactReadSerializer, StudentAffiliationReadSerializer,
    VisitReadSerializer, StudentWriteSerializer,
    StudentEligibilitySerializer, EligibilityTypeSerializer)
from compass.clients import (
    CompassPersonClient, PersonNotFoundException)
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseNotFound
from restclients_core.exceptions import DataFailureException
from rest_framework.response import Response
from rest_framework import status
from uw_sws.term import (
    get_current_term, get_next_term, get_term_after,
    get_term_by_year_and_quarter)
from uw_sws.registration import get_schedule_by_regid_and_term
from uw_sws.enrollment import get_enrollment_history_by_regid
from datetime import datetime

TERMS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Autumn"}


class StudentView(BaseAPIView):
    '''
    API endpoint returning a student's details

    /api/internal/student/[student_number|uwnetid]/
    '''
    def get(self, request, identifier):
        try:
            client = CompassPersonClient()
            if valid_uwnetid(identifier):
                person = client.get_person_by_uwnetid(identifier)
            elif valid_student_number(identifier):
                person = client.get_person_by_student_number(identifier)
            else:
                return Response('Invalid student identifier',
                                status=status.HTTP_400_BAD_REQUEST)
            person.photo_url = PhotoDAO().get_photo_url(person.uwregid)
            return JsonResponse(person.to_dict(), safe=False)
        except PersonNotFoundException:
            return HttpResponseNotFound()

    def post(self, request, identifier=None):
        access_groups = self.get_access_groups(request)
        try:
            # check user permissions for every group that the user belongs to
            for group in access_groups:
                self.validate_user_access(request, group.id)
            data = request.data
            system_key = data.get("system_key")
            if not valid_system_key(system_key):
                return Response('Invalid systemkey',
                                status=status.HTTP_400_BAD_REQUEST)

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
        if not valid_uwregid(uwregid):
            return Response('Invalid uwregid',
                            status=status.HTTP_400_BAD_REQUEST)

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
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

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
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request, systemkey, affiliation_id=None):
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            access_groups = self.get_access_groups(request)
            affiliation_data = request.data.get('affiliation')

            student = Student.objects.get(system_key=systemkey)

            affiliation_model_id = int(affiliation_data['affiliationId'])
            affiliation = Affiliation.objects.get(
                id=affiliation_model_id, access_group__in=access_groups)

            if affiliation_id:
                sa = StudentAffiliation.objects.get(id=affiliation_id)
                sa.affiliation = affiliation
            else:
                sa, _ = StudentAffiliation.objects.get_or_create(
                    student=student, affiliation=affiliation)

            sa.actively_advised = affiliation_data['actively_advised']
            sa.date = datetime.now().date()
            cohort_objects = []
            for c in affiliation_data['cohorts']:
                co, _ = Cohort.objects.get_or_create(
                    start_year=c['start_year'], end_year=c['end_year'])
                cohort_objects.append(co)

            sa.cohorts.clear()
            for cohort in cohort_objects:
                sa.cohorts.add(cohort)

            sa.save()

            serializer = StudentAffiliationReadSerializer(sa)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response("Unknown Student.",
                            status=status.HTTP_404_NOT_FOUND)
        except StudentAffiliation.DoesNotExist:
            return Response("Unknown Student Affiliation.",
                            status=status.HTTP_404_NOT_FOUND)
        except Affiliation.DoesNotExist:
            return Response("Unknown or Unpermitted Affiliation.",
                            status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response("User not authorized to update student data.",
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, systemkey, affiliation_id):
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            access_groups = self.get_access_groups(request)
            student = Student.objects.get(system_key=systemkey)
            student_affiliation = StudentAffiliation.objects.get(
                id=affiliation_id, student=student,
                affiliation__access_group__in=access_groups)
            student_affiliation.delete()
            return Response({}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response("Unknown Student.",
                            status=status.HTTP_404_NOT_FOUND)
        except StudentAffiliation.DoesNotExist:
            return Response("Unknown Student Affiliation.",
                            status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response("User not authorized to update student data.",
                            status=status.HTTP_401_UNAUTHORIZED)


class StudentVisitsView(BaseAPIView):
    '''
    API endpoint returning a list of visits for a student

    /api/internal/student/[systemkey]/visits/
    '''
    def get(self, request, systemkey):
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

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
        client = CompassPersonClient()
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

    /api/internal/student/[systemkey]/eligibility/
    '''
    def get(self, request, systemkey):
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

        access_groups = self.get_access_groups(request)
        eligibilities = []
        try:
            student = StudentEligibility.objects.get(
                student__system_key=systemkey)
            for e in student.eligibility.all():
                if e.access_group in access_groups:
                    eligibilities.append(EligibilityTypeSerializer(e).data)
        except StudentEligibility.DoesNotExist:
            pass

        return Response(eligibilities, status=status.HTTP_200_OK)

    def post(self, request, systemkey):
        if not valid_system_key(systemkey):
            return Response('Invalid systemkey',
                            status=status.HTTP_400_BAD_REQUEST)

        access_groups = self.get_access_groups(request)
        try:
            # check user permissions for every group that the user belongs to
            for group in access_groups:
                self.validate_user_access(request, group.id)

            eligibility_type_id = int(request.data.get("eligibility_type_id"))
            if eligibility_type_id < 0:
                return Response("Invalid Key or TypeID",
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                # update existing student record if one exists
                student = Student.objects.get(system_key=systemkey)
                eligibility_type = EligibilityType.objects.get(
                    id=eligibility_type_id, access_group__in=access_groups)
                s_e, _ = StudentEligibility.objects.get_or_create(
                    student=student)

                s_e.eligibility.add(eligibility_type)
                s_e.save()

                serializer = StudentEligibilitySerializer(s_e)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Student.DoesNotExist:
                return Response("Unknown Student.",
                                status=status.HTTP_404_NOT_FOUND)
            except EligibilityType.DoesNotExist:
                return Response("Unknown or Unpermitted Eligiblity.",
                                status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response("User not authorized to update student data.",
                            status=status.HTTP_401_UNAUTHORIZED)
