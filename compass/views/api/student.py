# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from restclients_core.exceptions import DataFailureException
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
        return JsonResponse(data.to_dict(), safe=False)


@method_decorator(verify_access(), name='dispatch')
class StudentScheduleView(View):
    '''
    API endpoint returning a student's class schedule details

    /api/internal/student/[uwregid]/schedule/
    '''
    def get(self, request, uwregid):
        cur_term = get_current_term()
        next_term = get_next_term()
        term_after = get_term_after(next_term)
        further_term = get_term_after(term_after)
        terms = [cur_term, next_term, term_after, further_term]
        schedules = {}
        for index, term in enumerate(terms):
            try:
                schedules[index] = \
                    get_schedule_by_regid_and_term(uwregid, term).json_data()
            except DataFailureException:
                continue
        return JsonResponse(schedules, safe=False)
