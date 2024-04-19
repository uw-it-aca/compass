# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import reverse
from compass.views.api import BaseAPIView
from compass.dao.person import (
    valid_uwnetid, get_students_by_system_keys, get_adviser_caseload,
    PersonNotFoundException, AdviserNotFoundException)
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

        contacts = Contact.objects.by_adviser(adviser_netid)

        if not len(contacts):
            return self.response_ok([])

        system_keys = [s['student__system_key'] for s in contacts]
        students = get_students_by_system_keys(system_keys)

        for contact in contacts:
            system_key = contact['student__system_key']
            contact['student'] = students[system_key]

        return self.response_ok(list(contacts))


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
