# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def _set_user(self, netid):
        self.client.force_login(User.objects.get_or_create(
            username=netid)[0])

    def get_response(self, url_name, netid, get_args=None, **kwargs):
        self._set_user(netid)
        url = reverse(url_name, **kwargs)
        return self.client.get(url, get_args, **kwargs)

    def _set_group(self, group):
        session = self.client.session
        session['samlUserdata'] = {'isMemberOf': [group]}
        session.save()

    def post_response(self, url_name, body, **kwargs):
        url = reverse(url_name, **kwargs)
        return self.client.post(url,
                                data=body,
                                content_type="application/json")
