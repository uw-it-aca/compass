# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.models import AppUser, Contact, ContactTopic, \
    ContactType, Student
from compass.serializers import ContactReadSerializer, \
    ContactWriteSerializer, ContactTopicSerializer, ContactTypeSerializer
from rest_framework.response import Response
from rest_framework import status


class ContactSaveView(BaseAPIView):
    '''
    API endpoint for saving a contact

    /api/internal/contact/save/
    '''

    def post(self, request):
        data = request.data
        contact_record = data['contact']
        system_key = data['system_key']
        contact_record['author'] = \
            AppUser.objects.upsert_appuser(uwnetid=request.user).id
        student, _ = Student.objects.get_or_create(system_key=system_key)
        contact_record['student'] = student.id
        try:
            # update existing contact record if one exists
            contact = Contact.objects.get(id=contact_record.get('id'))
            serializer = ContactWriteSerializer(contact, data=contact_record)
        except Contact.DoesNotExist:
            # create new contact record
            serializer = ContactWriteSerializer(data=contact_record)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ContactDetailView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/[contactid]/
    '''

    def get(self, request, contactid):
        queryset = Contact.objects.filter(id=contactid).get()
        serializer = ContactReadSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactTopicsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/topics/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)
        contact_topics = ContactTopic.objects.filter(
            access_group__in=access_groups)
        serializer = ContactTopicSerializer(contact_topics.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactTypesView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/types/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)
        contact_types = ContactType.objects.filter(
            access_group__in=access_groups)
        serializer = ContactTypeSerializer(contact_types.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
