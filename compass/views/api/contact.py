# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from compass.models import AccessGroup, AppUser, Contact, ContactTopic, \
    ContactType, Student
from compass.serializers import ContactReadSerializer, \
    ContactWriteSerializer, ContactTopicSerializer, ContactTypeSerializer
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from uw_saml.utils import get_attribute


@method_decorator(verify_access(), name='dispatch')
class BaseView(GenericAPIView):

    def get_access_groups(self, request):
        groups = get_attribute(request, 'isMemberOf') or []
        access_groups = AccessGroup.objects.filter(access_group_id__in=groups)
        return access_groups


class ContactListView(BaseView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/student/[systemkey]/contact/
    '''

    def get(self, request, systemkey):
        queryset = Contact.objects.filter(
            student__system_key=systemkey).order_by('-date', '-time')
        serializer = ContactReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactDetailView(BaseView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/contact/[contactid]/
    '''

    def get(self, request, contactid):
        queryset = Contact.objects.filter(id=contactid).get()
        serializer = ContactReadSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactSaveView(BaseView):
    '''
    API endpoint for saving a student contact

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


class ContactTopicsView(BaseView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/contact/topics/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)
        contact_topics = ContactTopic.objects.filter(
            access_group__in=access_groups)
        serializer = ContactTopicSerializer(contact_topics.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactTypesView(BaseView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/contact/types/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)
        contact_types = ContactType.objects.filter(
            access_group__in=access_groups)
        serializer = ContactTypeSerializer(contact_types.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
