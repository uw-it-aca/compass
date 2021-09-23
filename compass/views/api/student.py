# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import Student
from compass.serializers import StudentSerializer
from django.conf import settings
from django.db.models import F
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import JSONRenderer
from uw_saml.decorators import group_required


@method_decorator(group_required(settings.COMPASS_USERS_GROUP),
                  name='dispatch')
class BasePaginatedAPIView(GenericAPIView):

    renderer_classes = [JSONRenderer]
    pagination_class = LimitOffsetPagination


class StudentListView(BasePaginatedAPIView):
    '''
    API endpoint returning a list of students

    /api/internal/student/list/

    HTTP POST accepts the following dictionary parameters:
    * filters: dictionary of request filters
    '''
    def get(self, request, *args, **kwargs):
        student_qs = Student.objects.all()
        if request.query_params:
            filter_text = request.query_params.get("filter_text")
            filter_type = request.query_params.get("filter_type")
            if filter_type == "student-number":
                student_qs = student_qs.filter(
                    student_number__icontains=filter_text)
            elif filter_type == "student-name":
                student_qs = student_qs.filter(
                    student_name__icontains=filter_text)
            elif filter_type == "student-email":
                student_qs = student_qs.filter(
                    student_email__icontains=filter_text)
        paginated_queryset = self.paginate_queryset(student_qs)
        serializer = StudentSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class StudentDetailView(BasePaginatedAPIView):
    '''
    API endpoint returning a student's details

    /api/internal/student/detail/<student-number>

    HTTP POST accepts the following dictionary parameters:
    * filters: dictionary of request filters
    '''
    def get(self, request, student_number):
        student_qs = Student.objects.filter(student_number=student_number)
        serializer = StudentSerializer(student_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
