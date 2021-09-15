# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from compass.models import Term, Student
from compass.views.api import RESTDispatch
from django.db.models import F
from edw_clients.compass.dao import EDWCompassDAO


class EnrolledStudentsListView(RESTDispatch):
    '''
    API endpoint returning a list of users from the EDW

    /api/internal/edw/enrolled-students/

    HTTP POST accepts the following dictionary parameters:
    * filters: dictionary of request filters
    '''
    def post(self, request, *args, **kwargs):
        filters = json.loads(request.body.decode('utf-8'))
        page_num = filters["pageNum"]
        page_size = filters["pageSize"]
        start = (page_num - 1) * page_size
        end = page_num * page_size
        student_qs = Student.objects.all()
        if filters and filters.get("searchFilter"):
            filter_text = filters["searchFilter"]["filterText"]
            filter_type = filters["searchFilter"]["filterType"]
            if filter_type == "student-number":
                student_qs = student_qs.filter(student_number__icontains=filter_text)
            elif filter_type == "student-name":
                student_qs = student_qs.filter(student_name__icontains=filter_text)
            elif filter_type == "student-email":
                student_qs = student_qs.filter(student_email__icontains=filter_text)
        students = student_qs[start:end]
        student_values = students.values(
            'student_name',
            'student_number',
            'uw_net_id',
            'class_desc',
            'enrollment_status',
            'gender',
            major_full_name=F('major__major_full_name'),
            adviser_full_name=F('adviser__full_name')
        )
        return self.json_response(
            content=list(student_values))


class EnrolledStudentsCount(RESTDispatch):
    '''
    API endpoint returning a count of enrolled users from the EDW

    /api/internal/edw/enrolled-students-count/
    '''
    def post(self, request, *args, **kwargs):
        return self.json_response(
            content={'enrolled_students_count': Student.objects.count()})
