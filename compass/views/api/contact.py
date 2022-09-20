# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.models import AccessGroup, AppUser, Contact, ContactTopic, \
    ContactType, Student
from compass.serializers import ContactReadSerializer, \
    ContactWriteSerializer, ContactTopicSerializer, ContactTypeSerializer
from dateutil import parser
from django.core.exceptions import PermissionDenied
from django.conf import settings
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
        if any(app_user_group in contact.access_group.all() for
               app_user_group in access_groups):
            serializer = ContactReadSerializer(contact, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f"User not authorized to access contact "
                            f"{contactid}",
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, contactid=None):
        access_groups = self.get_access_groups(request)
        try:
            # if the user does not belong to any access groups, raise a
            # PermissionDenied error
            if not access_groups:
                raise PermissionDenied()
            # check user permissions for every group that the user belongs to
            for group in access_groups:
                self.validate_user_access(request, group.id)
            if not request.data:
                return Response([], status=status.HTTP_400_BAD_REQUEST)
            contact_record = request.data.get('contact')
            system_key = request.data.get('system_key')
            if contact_record is not None and system_key is not None:
                contact_record['app_user'] = \
                    AppUser.objects.upsert_appuser(uwnetid=request.user).id
                student, _ = Student.objects.get_or_create(
                    system_key=system_key)
                contact_record['student'] = student.id
                contact_record['access_group'] = [
                    access_group.pk for access_group in access_groups]
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


class ContactOMADView(BaseAPIView):
    '''
    API endpoint for ingesting OMAD contacts from the check-ins system

    /api/contact/omad/

    {
        adviser_netid: ""
        student_systemkey: "",
        contact_type: "",
        checkin_date: <CURRENT_TIMESTAMP>,
        source: "Compass"
    }
    '''

    def post(self, request):
        new_contact = request.data
        # confirm that the adviser is a member of the OMAD access group
        omad_access_group = AccessGroup.objects.get(
            access_group_id=settings.OMAD_ACCESS_GROUP_ID)
        user_access_groups = AccessGroup.objects.get_access_groups_for_netid(
            new_contact.adviser_netid)
        if omad_access_group not in user_access_groups:
            return Response(
                f"The specified app-user '{new_contact.adviser_netid}' is "
                f"not a member of the OMAD access group.",
                status=status.HTTP_400_BAD_REQUEST)
        # if the adviser is a member of the omad group, create an app-user and
        # student record for them if one doesn't already exist
        app_user = AppUser.objects.upsert_appuser(new_contact.adviser_netid)
        student, _ = Student.objects.get_or_create(
            system_key=new_contact.student_systemkey)
        # verify that the specified contact type exists in OMAD
        try:
            contact_type, _ = ContactType.objects.get(
                access_group=omad_access_group,
                name=new_contact.contact_type)
        except ContactType.DoesNotExist:
            return Response(
                f"The specified contact type "
                f"'{new_contact.contact_type}' does not exist for the OMAD"
                f"access group.",
                status=status.HTTP_400_BAD_REQUEST)
        # parse checkin date if one was specified
        if new_contact.get("checkin_date") is None:
            return Response("Check-in date not specified",
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                checkin_date = parser.parse(new_contact["checkin_date"])
            except parser.ParserError:
                return Response("Invalid check-in date",
                                status=status.HTTP_400_BAD_REQUEST)
        # create the new contact record
        contact = Contact()
        contact.app_user = app_user
        contact.access_group = omad_access_group
        contact.student = student
        contact.contact_type = contact_type
        contact.checkin_date = checkin_date
        contact.save()
        return Response(status=status.HTTP_201_CREATED)
