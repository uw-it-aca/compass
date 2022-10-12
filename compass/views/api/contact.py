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
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
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


@method_decorator(csrf_exempt, name='dispatch')
class ContactOMADView(GenericAPIView):
    '''
    API endpoint for ingesting OMAD contacts from the check-ins system

    /api/v1/contact/omad/

    {
        adviser_netid: ""
        student_systemkey: "",
        contact_type: "",
        checkin_date: <CURRENT_TIMESTAMP>,
        source: "Compass"
    }
    '''

    def parse_contact_type_str(self, contact_type_str, omad_access_group):
        try:
            contact_type, _ = ContactType.objects.get(
                access_group=omad_access_group,
                name=contact_type_str)
            return contact_type
        except ContactType.DoesNotExist:
            raise ValueError(
                f"The specified contact type "
                f"'{contact_type_str}' does not exist for the OMAD"
                f"access group.")

    def parse_checkin_date_str(self, checkin_date_str):
        # parse checkin date
        if checkin_date_str is None:
            raise ValueError("Check-in date not specified")
        else:
            try:
                return parser.parse(checkin_date_str)
            except parser.ParserError:
                raise ValueError("Invalid check-in date")

    def validate_adviser_netid(self, adviser_netid):
        if adviser_netid is None:
            raise ValueError("Adviser netid is not specified")

    def validate_student_systemkey(self, student_systemkey):
        if student_systemkey is None:
            raise ValueError("Student systemkey is not specified")
        else:
            if not student_systemkey.isdigit():
                raise ValueError("Student systemkey is not a positive integer")

    def post(self, request):
        contact_dict = request.data
        # confirm that the adviser is a member of the OMAD access group
        omad_access_group = AccessGroup.objects.get(
            access_group_id=settings.OMAD_ACCESS_GROUP_ID)
        if not AccessGroup.objects.is_access_group_member(
                contact_dict["adviser_netid"], omad_access_group):
            return Response(
                f"The specified app-user '{contact_dict['adviser_netid']}' is "
                f"not a member of the OMAD access group.",
                status=status.HTTP_400_BAD_REQUEST)
        # parse the contact dictionary
        try:
            # check that adviser netid is defined
            self.validate_adviser_netid(contact_dict.get("adviser_netid"))
            # check that system key is defined
            self.validate_student_systemkey(
                contact_dict.get("student_systemkey"))
            # parse checkin date to ensure it is in the correct format
            contact_dict["checkin_date"] = self.parse_checkin_date_str(
                contact_dict.get("checkin_date"))
            # verify that the specified contact type exists in OMAD
            contact_dict["contact_type"] = self.parse_contact_type_str(
                contact_dict.get("contact_type"), omad_access_group)
        except ValueError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        # if the adviser is a member of the omad group and the contact record
        # was successfully parsed, create an app-user and a student record for
        # them if one doesn't already exist
        app_user = AppUser.objects.upsert_appuser(
            contact_dict["adviser_netid"])
        student, _ = Student.objects.get_or_create(
            system_key=contact_dict["student_systemkey"])
        # create the new contact record
        contact = Contact()
        contact.app_user = app_user
        contact.student = student
        contact.contact_type = contact_dict["contact_type"]
        contact.checkin_date = contact_dict["checkin_date"]
        contact.save()
        contact.access_group.add(omad_access_group)
        return Response(status=status.HTTP_201_CREATED)
