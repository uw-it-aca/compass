# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.dao.photo import PhotoDAO
from compass.models import Student, Contact
from compass.serializers import ContactReadSerializer, StudentWriteSerializer
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseNotFound
from restclients_core.exceptions import DataFailureException
from rest_framework.response import Response
from rest_framework import status
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
from uw_sws.term import get_current_term, get_next_term, get_term_after, \
    get_term_by_year_and_quarter
from uw_sws.registration import get_schedule_by_regid_and_term


class StudentView(BaseAPIView):
    '''
    API endpoint returning a student's details

    /api/internal/student/[uwnetid]/
    '''
    def get(self, request, uwnetid):
        try:
            client = UWPersonClient()
            person = client.get_person_by_uwnetid(uwnetid)
            try:
                local_student = Student.objects.get(
                    system_key=person.student.system_key)
                person.student.compass_programs = [
                    program.id for program in local_student.programs.all()]
                person.photo_url = PhotoDAO().get_photo_url(
                    person.uwregid, "medium")
            except Student.DoesNotExist:
                person.student.compass_programs = []
            return JsonResponse(person.to_dict(), safe=False)
        except PersonNotFoundException:
            return HttpResponseNotFound()

    def post(self, request, uwnetid):
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
            student__system_key=systemkey).order_by('-date', '-time')
        serializer = ContactReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentTranscriptsView(BaseAPIView):
    '''
    API endpoint returning a list of transcripts for a student

    /api/internal/student/[uwregid]/transcripts/
    '''
    def get(self, request, uwregid):
        client = UWPersonClient()
        person = client.get_person_by_uwregid(uwregid)

        quarter_definitions = {
            1: "Winter",
            2: "Spring",
            3: "Summer",
            4: "Autumn",
        }

        transcripts = []
        for transcript in person.student.transcripts:
            term = get_term_by_year_and_quarter(
                transcript.tran_term.year,
                quarter_definitions[transcript.tran_term.quarter])
            try:
                class_schedule = get_schedule_by_regid_and_term(
                    uwregid, term)
                transcript.class_schedule = class_schedule.json_data()
            except DataFailureException:
                transcript.class_schedule = None
            transcripts.append(transcript.to_dict())
        return JsonResponse(transcripts, safe=False)
