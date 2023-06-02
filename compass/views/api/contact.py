# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView, JSONClientContentNegotiation, \
    TokenAPIView
from compass.models import AccessGroup, AppUser, Contact, ContactTopic, \
    ContactType, ContactMethod, Student
from compass.serializers import ContactReadSerializer, \
    ContactWriteSerializer, ContactTopicSerializer, ContactTypeSerializer, \
    ContactMethodSerializer
from dateutil import parser
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
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


class ContactMethodsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/methods/
    '''

    def get(self, request):
        # only load contact methods for the users access groups
        access_groups = self.get_access_groups(request)
        contact_methods = ContactMethod.objects.filter(
            access_group__in=access_groups)
        serializer = ContactMethodSerializer(contact_methods.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class ContactOMADView(TokenAPIView):
    '''
    API endpoint for ingesting contacts from the OMAD check-in system.

    /api/v1/contact/omad/

    {
        "adviser_netid": "<UW NETID>",
        "student_systemkey": "<System Key>",
        "contact_type": "<ContactType Slug",
        "checkin_date": "<CURRENT_TIMESTAMP>",
    }
    '''

    # Force JSON so clients aren't required to send ContentType header
    content_negotiation_class = JSONClientContentNegotiation

    def parse_contact_type_str(self, contact_type_str, access_group):
        try:
            return ContactType.objects.get(access_group=access_group,
                                           slug=contact_type_str)
        except ContactType.DoesNotExist:
            raise ValueError(
                f"Contact type '{contact_type_str}' does not exist "
                f"for the {access_group.name} access group.")

    def parse_checkin_date_str(self, checkin_date_str):
        # parse checkin date
        if checkin_date_str is None:
            raise ValueError("Check-in date not specified")
        else:
            try:
                dt = parser.parse(checkin_date_str)
                if dt.tzinfo is None:
                    raise ValueError("Invalid check-in date, missing timezone")
                return dt
            except parser.ParserError as e:
                raise ValueError(f"Invalid check-in date: {e}")

    def validate_adviser_netid(self, adviser_netid):
        if adviser_netid is None:
            raise ValueError("Missing adviser netid")

    def validate_student_systemkey(self, student_systemkey):
        if student_systemkey is None:
            raise ValueError("Missing student systemkey")

        try:
            if not student_systemkey.isdigit():
                raise ValueError("Student systemkey is not a positive integer")
        except AttributeError as e:
            raise ValueError(f"Invalid student systemkey: {e}")

    def post(self, request):
        contact_dict = request.data
        try:
            access_group = AccessGroup.objects.by_name("OMAD")
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
                contact_dict.get("contact_type"), access_group)
        except AccessGroup.DoesNotExist as e:
            return Response(repr(e), status=status.HTTP_501_NOT_IMPLEMENTED)
        except ValueError as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)
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
        contact.source = "Checkin"
        contact.save()
        contact.access_group.add(access_group)
        return Response(status=status.HTTP_201_CREATED)
