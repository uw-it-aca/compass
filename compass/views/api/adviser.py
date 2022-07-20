# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import BaseAPIView
from compass.decorators import verify_access
from compass.models import Contact
from compass.serializers import ContactReadSerializer
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from uw_person_client import UWPersonClient


@method_decorator(verify_access(), name='dispatch')
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
        for contact in contact_queryset:
            contact_dict = ContactReadSerializer(contact, many=False).data
            student = client.get_person_by_system_key(
                contact.student.system_key)
            contact_dict["student"] = student.to_dict()
            contacts.append(contact_dict)
        return JsonResponse([contact for contact in contacts], safe=False)


@method_decorator(verify_access(), name='dispatch')
class AdviserCaseloadView(BaseAPIView):
    '''
    API endpoint returning a list of contacts of an adviser

    /api/internal/adviser/<adviser_netid>/caseload/
    '''

    def get(self, request, adviser_netid):
        client = UWPersonClient()
        persons = client.get_persons_by_adviser_netid(adviser_netid)
        return JsonResponse([person.to_dict() for person in persons],
                            safe=False)
