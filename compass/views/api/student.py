# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.decorators import verify_access
from compass.models import Student, Contact
from compass.serializers import ContactReadSerializer, StudentWriteSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from restclients_core.exceptions import DataFailureException
from rest_framework.response import Response
from rest_framework import status
from uw_person_client import UWPersonClient
from uw_sws.term import get_current_term, get_next_term, get_term_after
from uw_sws.registration import get_schedule_by_regid_and_term


@method_decorator(verify_access(), name='dispatch')
class StudentListView(View):
    '''
    API endpoint returning a list of students

    /api/internal/student/
    '''
    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")
        page_size = request.GET.get("page_size")
        client = UWPersonClient()
        data = client.get_active_students(page=page, page_size=page_size)
        return JsonResponse([item.to_dict() for item in data], safe=False)


@method_decorator(verify_access(), name='dispatch')
class StudentDetailView(View):
    '''
    API endpoint returning a student's details

    /api/internal/student/[uwnetid]/
    '''
    def get(self, request, uwnetid):
        client = UWPersonClient()
        data = client.get_person_by_uwnetid(uwnetid)
        try:
            local_student = Student.objects.get(
                system_key=data.student.system_key)
            data.student.compass_programs = [
                program.id for program in local_student.programs.all()]
            data.student.compass_special_programs = [
                sp.id for sp in local_student.special_programs.all()]
        except Student.DoesNotExist:
            data.student.compass_programs = []
            data.student.compass_special_programs = []
        return JsonResponse(data.to_dict(), safe=False)


class StudentSaveView(BaseAPIView):
    '''
    API endpoint for saving student programs

    /api/internal/student/save/
    '''

    def post(self, request):
        data = request.data
        system_key = data["system_key"]
        student_record = {}
        student_record['system_key'] = system_key
        student_record['programs'] = data['programs']
        student_record['special_programs'] = data['special_programs']
        try:
            # update existing student record if one exists
            student, _ = Student.objects.get_or_create(system_key=system_key)
            serializer = StudentWriteSerializer(student, data=student_record)
        except Student.DoesNotExist:
            # create new student record
            serializer = StudentWriteSerializer(data=student_record)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@method_decorator(verify_access(), name='dispatch')
class StudentSchedulesView(View):
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
