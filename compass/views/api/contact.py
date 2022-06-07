# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from compass.models import Contact
from compass.serializers import ContactSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from uw_person_client import UWPersonClient


class ContactResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


@method_decorator(verify_access(), name='dispatch')
class ContactListView(GenericAPIView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/contact/[systemkey]/
    '''

    renderer_classes = [JSONRenderer]
    pagination_class = ContactResultsSetPagination

    def get(self, request, systemkey):
        queryset = Contact.objects.filter(
            student__system_key=systemkey).order_by('-date', '-time')
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = ContactSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
