# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.dao.person import valid_uwnetid
from compass.dao.photo import PhotoDAO
from compass.clients import (
    CompassPersonClient, PersonNotFoundException, AdviserNotFoundException)
from compass.models import Contact
from compass.serializers import ContactReadSerializer
import datetime


class AdviserContactsView(BaseAPIView):
    """
    API endpoint returning a list of contacts of an adviser for previous 3 days
    /api/internal/adviser/<adviser_netid>/contact/
    """

    def get(self, request, adviser_netid):
        if not valid_uwnetid(adviser_netid):
            return self.response_badrequest('Invalid uwnetid')

        client = CompassPersonClient()
        earliest_contact_date = datetime.datetime.now(
            datetime.timezone.utc) - datetime.timedelta(hours=72)
        contact_queryset = Contact.objects.filter(
            app_user__uwnetid=adviser_netid,
            checkin_date__gte=earliest_contact_date).all()
        contacts = []
        photo_dao = PhotoDAO()
        for contact in contact_queryset:
            contact_dict = ContactReadSerializer(contact, many=False).data
            try:
                person = client.get_person_by_system_key(
                    contact.student.system_key
                )
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

        client = CompassPersonClient()
        try:
            persons = client.get_adviser_caseload(adviser_netid)
        except AdviserNotFoundException:
            persons = []
        photo_dao = PhotoDAO()
        for person in persons:
            person.photo_url = photo_dao.get_photo_url(person.uwregid)

        return self.response_ok([person.to_dict() for person in persons])
