# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client
from rest_framework.authtoken.models import Token

from compass.models import AccessGroup, AppUser, Contact
from compass.tests import ApiTest
from compass.views.api.contact import ContactOMADView


class ContactAPITest(ApiTest):
    API_TOKEN = None
    WRONG_API_TOKEN = None

    def setUp(self):
        super().setUp()
        AccessGroup(name="OMAD", access_group_id="u_astra_group1").save()

        user = User.objects.create_user(username='omad-compass-api',
                                        password='12345')
        self.API_TOKEN = Token.objects.create(user=user).key

        other_user = User.objects.create_user(username='foobar',
                                              password='12345')
        self.WRONG_API_TOKEN = Token.objects.create(user=other_user).key

    def test_api_auth(self):
        test_request = {
            "adviser_netid": "javerage",
            "student_systemkey": "12345",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass"
        }

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        response = self.post_response('contact_omad',
                                      body=test_request)
        self.assertEqual(response.status_code, 201)
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION="BAD TOKEN")

        response = self.post_response('contact_omad',
                                      test_request)
        self.assertEqual(response.status_code, 401)

        wrong_token_str = f"Token {self.WRONG_API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=wrong_token_str)

        response = self.post_response('contact_omad',
                                      body=test_request)
        self.assertEqual(response.status_code, 401)

    @patch('compass.views.api.contact.validate_contact_post_data')
    @patch('compass.views.api.contact.OMADContactQueue')
    def test_omad_post(self, mock_queue_cls, mock_validate):
        mock_queued = MagicMock()
        mock_queue_cls.objects.create.return_value = mock_queued

        mock_view = ContactOMADView()
        mock_request = MagicMock()
        mock_request.data = {}
        mock_request.user.username = "omad-compass-api"
        response = mock_view.post(mock_request)

        # assert contact was queued
        mock_queue_cls.objects.create.assert_called_once()
        # assert validation was called with the contact data
        mock_validate.assert_called_once_with(mock_request.data)
        self.assertEqual(response.status_code, 201)

    @patch('compass.views.api.contact.validate_contact_post_data')
    @patch('compass.views.api.contact.OMADContactQueue')
    def test_omad_post_validation_error_does_not_queue(self, mock_queue_cls,
                                                      mock_validate):
        mock_validate.side_effect = ValueError("Missing adviser netid")

        mock_view = ContactOMADView()
        mock_request = MagicMock()
        mock_request.data = {}
        mock_request.user.username = "omad-compass-api"

        response = mock_view.post(mock_request)

        mock_queue_cls.objects.create.assert_not_called()
        self.assertEqual(response.status_code, 400)

    def test_syskey_leading_zero(self):
        test_nopad = {
            "adviser_netid": "javerage",
            "student_systemkey": "1234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass"
        }

        test_pad = {
            "adviser_netid": "javerage",
            "student_systemkey": "001234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass"
        }

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        # create without padding
        self.post_response('contact_omad',
                           body=test_nopad)
        call_command('process_omad_contacts')
        contacts = Contact.objects.all()
        self.assertEqual(contacts[0].student.system_key, "001234567")

        # create with padding
        self.post_response('contact_omad',
                           body=test_pad)
        call_command('process_omad_contacts')
        contacts = Contact.objects.all()
        self.assertEqual(contacts[1].student.system_key, "001234567")

    def test_trans_id(self):
        test_noid = {
            "adviser_netid": "javerage",
            "student_systemkey": "1234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass"
        }

        test_id = {
            "adviser_netid": "javerage",
            "student_systemkey": "001234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass",
            "trans_id": 1234567890
        }

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        self.post_response('contact_omad',
                           body=test_noid)
        self.post_response('contact_omad',
                           body=test_id)
        call_command('process_omad_contacts')
        contacts = Contact.objects.all()
        self.assertEqual(len(contacts), 2)
        self.assertIsNone(contacts[0].trans_id)
        self.assertEqual(contacts[1].trans_id, 1234567890)

    @patch('compass.dao.group.is_member_of_group')
    def test_delete(self, mock_is_member, return_value=True):
        test_id = {
            "adviser_netid": "javerage",
            "student_systemkey": "001234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass",
            "trans_id": 1234567890
        }

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        self.post_response('contact_omad',
                           body=test_id)
        call_command('process_omad_contacts')
        contacts = Contact.objects.all()

        c_id = contacts[0].id
        self.delete_response('contact_edit_view',
                             'javerage',
                             kwargs={'contactid': c_id})

        contacts = Contact.objects.all()
        self.assertEqual(len(contacts), 0)

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_put(self, mock_is_member):
        test_checkin = {
            "adviser_netid": "javerage",
            "student_systemkey": "001234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass",
            "trans_id": 1234567890
        }

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        self.post_response('contact_omad',
                                  body=test_checkin)
        call_command('process_omad_contacts')

        contact = Contact.objects.get(id=1)
        self.assertIsNone(contact.notes)
        self.assertEqual(contact.app_user.uwnetid, "javerage")

        put_body = {
            "contact": {
                "id": 1,
                "app_user": {
                    "id": 1,
                    "uwnetid": "jbothell"
                },
                "student": 1234,
                "created_date": "2023-12-20T23:31:55.156661Z",
                "checkin_date": "2023-12-01T15:18:00",
                "notes": "test note",
                "actions": "test1",
                "contact_type": 1,
                "contact_method": 1,
                "contact_topics": [
                    1
                ],
                "source": "Compass",
                "trans_id": None,
                "access_group": [
                    {
                        "id": 1,
                        "name": "ADVISOR",
                        "access_group_id": "u_test_group"
                    }
                ]
            },
            "system_key": "001111111"
        }
        AppUser(uwnetid="jbothell").save()
        r = self.put_response('contact_edit_view',
                              "jbothell",
                              put_body,
                              kwargs={'contactid': 1})
        self.assertEqual(r.status_code, 200)
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.notes, "test note")
        self.assertEqual(contact.app_user.uwnetid, "javerage")

        r = self.put_response('contact_edit_view',
                              "javerage",
                              put_body,
                              kwargs={'contactid': 1})
        self.assertEqual(r.status_code, 200)

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_post(self, mock_is_member):
        post_body = {
            "contact": {
                "contact_topics": [
                    1
                ],
                "checkin_date": "2023-12-22T11:15",
                "notes": "test",
                "contact_type": 1,
                "contact_method": 3
            },
            "system_key": "002365572"
        }
        r = self.post_response('contact_create_view',
                               'javerage',
                               post_body)
        contacts = Contact.objects.all()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(contacts[0].notes, "test")

    def test_omad_queue_view(self):
        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        payload = {
            "adviser_netid": "javerage",
            "student_systemkey": "12345",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass"
        }

        post_response = self.post_response('contact_omad', body=payload)
        self.assertEqual(post_response.status_code, 201)

        # Use support-group session auth for the internal admin endpoint.
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self._set_user('jadviser')
        self._set_group('u_test_group')

        response = self.get_response('omad_contact_queue_view')
        self.assertEqual(response.status_code, 200)

        queue_rows = response.json()
        self.assertEqual(len(queue_rows), 1)
        self.assertIn('id', queue_rows[0])
        self.assertIn('json', queue_rows[0])
