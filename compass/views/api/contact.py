# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from compass.models import AccessGroup, AppUser, Contact, ContactType, \
    Student
from compass.serializers import ContactSerializer, ContactTopicSerializer, \
    ContactTypeSerializer
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from uw_saml.utils import get_attribute


@method_decorator(verify_access(), name='dispatch')
class ContactListView(GenericAPIView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/student/[systemkey]/contact/
    '''

    renderer_classes = [JSONRenderer]

    def get(self, request, systemkey):
        queryset = Contact.objects.filter(
            student__system_key=systemkey).order_by('-date', '-time')
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, systemkey):
        contact_record = request.data
        contact_record['author'] = \
            AppUser.objects.upsert_appuser(uwnetid=request.user).id
        student, _ = Student.objects.get_or_create(system_key=systemkey)
        contact_record['student'] = student.id
        serializer = ContactSerializer(data=contact_record)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@method_decorator(verify_access(), name='dispatch')
class ContactTopicsView(GenericAPIView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/student/[systemkey]/contact/topics/
    '''

    def get(self, request, systemkey):
        groups = get_attribute(request, 'isMemberOf') or []
        access_groups = AccessGroup.objects.filter(access_group_id__in=groups)
        topics = []
        for group in access_groups:
            for contact_topic in group.contact_topics.all():
                topics.append(contact_topic)
        serializer = ContactTopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(verify_access(), name='dispatch')
class ContactTypesView(GenericAPIView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/student/[systemkey]/contact/types/
    '''

    def get(self, request, systemkey):
        queryset = ContactType.objects.all()
        serializer = ContactTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
