# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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
        photo_dao = PhotoDAO()
        for contact in Contact.objects.by_adviser(adviser_netid):
            contact_dict = ContactReadSerializer(contact, many=False).data
            try:
                person = get_person_by_system_key(contact.student.system_key)
                person.photo_url = photo_dao.get_photo_url(person.uwregid)
                contact_dict["student"] = person.to_dict()
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

        photo_dao = PhotoDAO()
        students = []
        for row in queryset:
            row['photo_url'] = photo_dao.get_photo_url(row['uwregid'])
            students.append(row)

        return self.response_ok(students)
