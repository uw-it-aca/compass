# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.dao import current_datetime_utc
from compass.views.api import (
    BaseAPIView, JSONClientContentNegotiation, TokenAPIView)
from compass.models import (
    AccessGroup, AppUser, Contact, ContactTopic, ContactType, ContactMethod,
    Student)
from compass.serializers import (
    ContactReadSerializer, ContactWriteSerializer, ContactTopicSerializer,
    ContactTypeSerializer, ContactMethodSerializer)
from dateutil import parser
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from userservice.user import UserService
from logging import getLogger
from uw_person_client.exceptions import PersonNotFoundException


logger = getLogger(__name__)


class ContactView(BaseAPIView):
    '''
    API endpoint for contact

    /api/internal/contact/(contactid)/
    '''
    def get(self, request, contactid):
        try:
            contact = Contact.objects.get(id=contactid)
        except Contact.DoesNotExist:
            return self.response_notfound()

        serializer = ContactReadSerializer(contact, many=False)
        return self.response_ok(serializer.data)

    def delete(self, request, contactid):
        try:
            contact = Contact.objects.get(id=contactid)
        except Contact.DoesNotExist:
            return self.response_notfound()

        try:
            contact_ags = contact.access_group.all()
            self.valid_user_permission(request,
                                       access_groups=contact_ags,
                                       allow_override=False,
                                       require_manager=True)
        except PermissionDenied:
            return self.response_unauthorized()

        contact.delete()
        logger.info("Contact deleted: %s" % contactid)
        return self.response_ok({})

    def put(self, request, contactid):
        contact_record = request.data.get('contact')
        try:
            contact = Contact.objects.get(id=contactid)
        except Contact.DoesNotExist:
            return self.response_badrequest("Unrecognized ContactId")

        try:
            us = UserService()
            app_user = AppUser.objects.get(uwnetid=us.get_user())
        except AppUser.DoesNotExist:
            return self.response_unauthorized("Unrecognized AppUser")

        try:
            contact_ags = contact.access_group.all()
            if contact.app_user == app_user:
                self.valid_user_permission(request,
                                           access_groups=contact_ags,
                                           allow_override=False)
            else:
                self.valid_user_permission(request,
                                           access_groups=contact_ags,
                                           allow_override=False,
                                           require_manager=True)
        except PermissionDenied:
            return self.response_unauthorized()

        # Don't update these fields, use data from existing contact record
        contact_record['student'] = contact.student.id
        contact_record['access_group'] = [ag.id for ag in
                                          contact.access_group.all()]
        contact_record['app_user'] = contact.app_user.id
        contact_record['created_date'] = contact.created_date

        serializer = ContactWriteSerializer(contact, data=contact_record)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Contact {contactid} updated: "
                        f"{serializer.data}")
            return self.response_ok(serializer.data)
        return self.response_badrequest(serializer.errors)

    def post(self, request):
        us = UserService()
        try:
            self.valid_user_permission(request, allow_override=False)
            access_group = self.get_access_group(request)

        except PermissionDenied:
            return self.response_unauthorized()

        if not request.data:
            return self.response_badrequest()

        contact_record = request.data.get('contact')
        system_key = request.data.get('system_key')

        if contact_record is None or system_key is None:
            return self.response_badrequest(
                "system_key and contact are required")

        contact_record['app_user'] = AppUser.objects.upsert_appuser(
            uwnetid=us.get_user()).id
        student, _ = Student.objects.get_or_create(system_key=system_key)
        contact_record['student'] = student.id
        contact_record['access_group'] = [access_group.id]
        try:
            if isinstance(contact_record['contact_type'], str):
                slug = slugify(contact_record['contact_type'])
                contact_record['contact_type'] = \
                    ContactType.objects.get(slug=slug).id
            if isinstance(contact_record['contact_method'], str):
                slug = slugify(contact_record['contact_method'])
                contact_record['contact_method'] = \
                    ContactMethod.objects.get(slug=slug).id
            if isinstance(contact_record['contact_topics'], list):
                topics = []
                for t in contact_record['contact_topics']:
                    if isinstance(t, str):
                        slug = slugify(t)
                        topics.append(
                            ContactTopic.objects.get(
                                slug=slug).id)
                    else:
                        topics.append(t)

                contact_record['contact_topics'] = topics

            if 'checkin_date' not in contact_record:
                contact_record['checkin_date'] = current_datetime_utc()

        except (KeyError, ContactType.DoesNotExist,
                ContactMethod.DoesNotExist,
                ContactTopic.DoesNotExist):
            return self.response_badrequest("Unrecognized Contact Values")

        serializer = ContactWriteSerializer(data=contact_record)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"Contact saved for student {system_key}: "
                        f"{serializer.data}")
            return self.response_created(serializer.data)
        return self.response_badrequest(serializer.errors)


class ContactTopicsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/topics/
    '''

    def get(self, request):
        try:
            access_group = self.valid_user_permission(request)
        except PermissionDenied:
            return self.response_unauthorized()

        contact_topics = ContactTopic.objects.filter(
            access_group=access_group)
        serializer = ContactTopicSerializer(contact_topics.all(), many=True)
        return self.response_ok(serializer.data)


class ContactTypesView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/types/
    '''

    def get(self, request):
        try:
            access_group = self.valid_user_permission(request)
        except PermissionDenied:
            return self.response_unauthorized()

        contact_types = ContactType.objects.filter(
            access_group=access_group)
        serializer = ContactTypeSerializer(contact_types.all(), many=True)
        return self.response_ok(serializer.data)


class ContactMethodsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for the user's access group

    /api/internal/contact/methods/
    '''

    def get(self, request):
        try:
            access_group = self.valid_user_permission(request)
        except PermissionDenied:
            return self.response_unauthorized()

        contact_methods = ContactMethod.objects.filter(
            access_group=access_group)
        serializer = ContactMethodSerializer(contact_methods.all(), many=True)
        return self.response_ok(serializer.data)


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
        "trans_id": <TRANSACTION ID>,
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

    @staticmethod
    def pad_student_systemkey(student_systemkey):
        return student_systemkey.zfill(9)

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
        try:
            app_user = AppUser.objects.upsert_appuser(
                contact_dict["adviser_netid"])
        except PersonNotFoundException as e:
            logger.error("ContactOMADView: Person not found for "
                         "adviser_netid: %s" % contact_dict["adviser_netid"])
            return Response("Person record for adviser not found",
                            status=status.HTTP_400_BAD_REQUEST)

        student_systemkey = self.pad_student_systemkey(
            contact_dict["student_systemkey"])
        # student_systemkey = contact_dict["student_systemkey"]
        student, _ = Student.objects.get_or_create(
            system_key=student_systemkey)
        # create the new contact record
        contact = Contact()
        contact.app_user = app_user
        contact.student = student
        contact.contact_type = contact_dict["contact_type"]
        contact.checkin_date = contact_dict["checkin_date"]
        contact.source = "Checkin"
        try:
            contact.trans_id = contact_dict["trans_id"]
        except KeyError:
            pass
        contact.save()
        contact.access_group.add(access_group)
        logger.info(f"Checkin contact {contact.contact_type} added for "
                    f"student {student.system_key}")
        return Response(status=status.HTTP_201_CREATED)
