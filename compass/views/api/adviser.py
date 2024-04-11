# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import reverse
from compass.views.api import BaseAPIView
from compass.dao.person import (
    valid_uwnetid, get_person_by_system_key, get_adviser_caseload,
    PersonNotFoundException, AdviserNotFoundException)
from compass.dao.photo import PhotoDAO
from compass.models import Contact
from compass.serializers import ContactReadSerializer


class AdviserCheckInsView(BaseAPIView):
    """
    API endpoint returning a list of checkins of an adviser
    /api/internal/adviser/<adviser_netid>/checkins/
    """

    def get(self, request, adviser_netid):
        if not valid_uwnetid(adviser_netid):
            return self.response_badrequest('Invalid uwnetid')

        contacts = []
        photo_key = PhotoDAO().generate_photo_key()
        for contact in Contact.objects.by_adviser(adviser_netid):
            contact_dict = ContactReadSerializer(contact, many=False).data
            try:
                person = get_person_by_system_key(contact.student.system_key)
                person_dict = person.to_dict()
                person_dict['photo_url'] = reverse('photo', kwargs={
                    'uwregid': person.uwregid,
                    'photo_key': photo_key})
                contact_dict["student"] = person_dict
                contacts.append(contact_dict)
            except PersonNotFoundException:
                pass
        return self.response_ok([contact for contact in contacts])


class AdviserCaseloadView(BaseAPIView):
    """
    API endpoint returning a list of contacts of an adviser
    /api/internal/adviser/<adviser_netid>/caseload/
    """

    def get(self, request, adviser_netid):
        if not valid_uwnetid(adviser_netid):
            return self.response_badrequest('Invalid uwnetid')

        try:
            queryset = get_adviser_caseload(adviser_netid)
        except AdviserNotFoundException:
            queryset = []

        return self.response_ok(list(queryset))
