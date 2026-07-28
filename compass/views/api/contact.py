# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from logging import getLogger

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from userservice.user import UserService

from compass.dao import current_datetime_utc
from compass.dao.contact import (
    get_omad_access_group,
)
from compass.dao.contact import (
    parse_checkin_date_str as _parse_checkin_date_str,
)
from compass.dao.contact import (
    parse_contact_type_str as _parse_contact_type_str,
)
from compass.dao.contact import (
    validate_adviser_netid as _validate_adviser_netid,
)
from compass.dao.contact import (
    validate_student_systemkey as _validate_student_systemkey,
)
from compass.models import (
    AccessGroup,
    AppUser,
    Contact,
    ContactMethod,
    ContactTopic,
    ContactType,
    Student,
)
from compass.serializers import (
    ContactMethodSerializer,
    ContactReadSerializer,
    ContactTopicSerializer,
    ContactTypeSerializer,
    ContactWriteSerializer,
)
from compass.utils import format_system_key
from compass.views.api import BaseAPIView, JSONClientContentNegotiation, TokenAPIView

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
        logger.info(f"Contact deleted: {contactid}")
        return self.response_ok({})

    def put(self, request, contactid):
        contact_record = request.data.get('contact')
        try:
            contact = Contact.objects.get(id=contactid)
        except Contact.DoesNotExist:
            return self.response_badrequest("Unrecognized ContactId")

        try:
            app_user = self.get_app_user()
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
                    ContactType.objects.get(
                        access_group=access_group,
                        slug=slug,
                    ).id
            if isinstance(contact_record['contact_method'], str):
                slug = slugify(contact_record['contact_method'])
                contact_record['contact_method'] = \
                    ContactMethod.objects.get(
                        access_group=access_group,
                        slug=slug,
                    ).id
            if isinstance(contact_record['contact_topics'], list):
                topics = []
                for t in contact_record['contact_topics']:
                    if isinstance(t, str):
                        slug = slugify(t)
                        topics.append(
                            ContactTopic.objects.get(
                                access_group=access_group,
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
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
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
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
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
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
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

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.username != getattr(
                settings, 'OMAD_CONTACT_TOKEN_USER', None):
            raise AuthenticationFailed("Unauthorized")

    def validate_adviser_netid(self, adviser_netid):
        _validate_adviser_netid(adviser_netid)

    def validate_student_systemkey(self, student_systemkey):
        _validate_student_systemkey(student_systemkey)

    def parse_checkin_date_str(self, checkin_date_str):
        return _parse_checkin_date_str(checkin_date_str)

    def parse_contact_type_str(self, contact_type_str, access_group):
        return _parse_contact_type_str(contact_type_str, access_group)

    def post(self, request):
        try:
            omad_access_group = get_omad_access_group()
            self.validate_adviser_netid(request.data.get("adviser_netid"))
            self.validate_student_systemkey(
                request.data.get("student_systemkey"))
            request.data["checkin_date"] = self.parse_checkin_date_str(
                request.data.get("checkin_date"))
            request.data["contact_type"] = self.parse_contact_type_str(
                request.data.get("contact_type"), omad_access_group)
        except (ValueError, AccessGroup.DoesNotExist) as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)

        app_user = AppUser.objects.upsert_appuser(
            request.data["adviser_netid"])
        student, _ = Student.objects.get_or_create(
            system_key=format_system_key(
                request.data.get("student_systemkey")))
        contact = Contact()
        contact.app_user = app_user
        contact.student = student
        contact.contact_type = request.data["contact_type"]
        contact.checkin_date = request.data["checkin_date"]
        try:
            contact.trans_id = request.data["trans_id"]
        except KeyError:
            pass
        contact.save()
        contact.access_group.add(omad_access_group)
        return Response(status=status.HTTP_201_CREATED)
