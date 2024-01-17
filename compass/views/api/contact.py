# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.dao import current_datetime_utc
from compass.views.api import (
    BaseAPIView, JSONClientContentNegotiation, TokenAPIView)
from compass.models import (
    AccessGroup, AppUser, Contact, ContactTopic, ContactType, ContactMethod,
    Student, OMADContactQueue)
from compass.serializers import (
    ContactReadSerializer, ContactWriteSerializer, ContactTopicSerializer,
    ContactTypeSerializer, ContactMethodSerializer)
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from userservice.user import UserService
from logging import getLogger
import json
from compass.dao.contact import validate_contact_post_data
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

    def post(self, request):
        contact_dict = request.data
        queued_contact = OMADContactQueue.objects.create(
            json=json.dumps(contact_dict)
        )
        logger.info(f"OMAD contact queued, id: {queued_contact.id}")
        try:
            validate_contact_post_data(contact_dict)
        except AccessGroup.DoesNotExist as e:
            return Response(repr(e), status=status.HTTP_501_NOT_IMPLEMENTED)
        except ValueError as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)
        except PersonNotFoundException as e:
            return Response("Person record for adviser not found",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
