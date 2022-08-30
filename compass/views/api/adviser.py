# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.dao.photo import PhotoDAO
from compass.clients import CompassPersonClient
from compass.models import Contact
from compass.serializers import ContactReadSerializer
from django.http import JsonResponse
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import AdviserNotFoundException


class AdviserContactsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts of an adviser

    /api/internal/adviser/<adviser_netid>/contact/
    '''

    def get(self, request, adviser_netid):
        client = UWPersonClient()
        contact_queryset = Contact.objects.filter(
            author__uwnetid=adviser_netid).all()
        contacts = []
        photo_dao = PhotoDAO()
        for contact in contact_queryset:
            contact_dict = ContactReadSerializer(contact, many=False).data
            person = client.get_person_by_system_key(
                contact.student.system_key)
            person.photo_url = photo_dao.get_photo_url(person.uwregid)
            contact_dict["student"] = person.to_dict()
            contacts.append(contact_dict)
        return JsonResponse([contact for contact in contacts], safe=False)


class AdviserCaseloadView(BaseAPIView):
    '''
    API endpoint returning a list of contacts of an adviser

    /api/internal/adviser/<adviser_netid>/caseload/
    '''

    def get(self, request, adviser_netid):
        client = CompassPersonClient()
        try:
            persons = client.get_adviser_caseload(adviser_netid)
        except AdviserNotFoundException:
            persons = []
        photo_dao = PhotoDAO()
        for person in persons:
            person.photo_url = photo_dao.get_photo_url(person.uwregid)
        return JsonResponse([person.to_dict() for person in persons],
                            safe=False)
