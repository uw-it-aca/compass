# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from uw_saml.decorators import group_required
from uw_person_client import UWPersonClient


@method_decorator(group_required(settings.COMPASS_USERS_GROUP),
                  name='dispatch')
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

@method_decorator(group_required(settings.COMPASS_USERS_GROUP),
                  name='dispatch')
class StudentDetailView(View):
    '''
    API endpoint returning a student's details

    /api/internal/student/<student-number>
    '''
    def get(self, request, student_number):
        client = UWPersonClient()
        data = client.get_person_by_student_number(student_number)
        return JsonResponse(data.to_dict(), safe=False)
