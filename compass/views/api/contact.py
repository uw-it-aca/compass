# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.models import AppUser, Contact, ContactTopic, \
    ContactType, Student
from compass.serializers import ContactReadSerializer, \
    ContactWriteSerializer, ContactTopicSerializer, ContactTypeSerializer
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


class ContactView(BaseAPIView):
    '''
    API endpoint for contact

    /api/internal/contact/(contactid)/
    '''
    def get(self, request, contactid):
        contact = Contact.objects.filter(id=contactid).get()
        access_groups = self.get_access_groups(request)
        if contact.access_group in access_groups:
            serializer = ContactReadSerializer(contact, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f"User not authorized to access contact "
                            f"{contactid}",
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, contactid=None):
        access_groups = self.get_access_groups(request)
        try:
            # check user permissions for every group that the user belongs to
            for group in access_groups:
                self.validate_user_access(request, group.id)
            if not request.data:
                return Response([], status=status.HTTP_400_BAD_REQUEST)
            contact_record = request.data.get('contact')
            system_key = request.data.get('system_key')
            if contact_record is not None and system_key is not None:
                contact_record['author'] = \
                    AppUser.objects.upsert_appuser(uwnetid=request.user).id
                student, _ = Student.objects.get_or_create(
                    system_key=system_key)
                contact_record['student'] = student.id
                try:
                    # update existing contact record if one exists
                    contact = Contact.objects.get(id=contactid)
                    serializer = ContactWriteSerializer(
                        contact, data=contact_record)
                except Contact.DoesNotExist:
                    # create new contact record
                    serializer = ContactWriteSerializer(data=contact_record)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            group_names = [group.name for group in access_groups]
            return Response(f"User not authorized to access create new "
                            f"student contacts for access groups "
                            f"{', '.join(group_names)}",
                            status=status.HTTP_401_UNAUTHORIZED)


class ContactTopicsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/topics/
    '''

    def get(self, request):
        # only load contact topics for the users access groups
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
        # only load contact types for the users access groups
        access_groups = self.get_access_groups(request)
        contact_types = ContactType.objects.filter(
            access_group__in=access_groups)
        serializer = ContactTypeSerializer(contact_types.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
