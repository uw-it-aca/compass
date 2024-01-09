# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import Client
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from compass.views.api.contact import ContactOMADView
from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, AppUser
from django.core.management import call_command
from rest_framework.authtoken.models import Token


class ContactAPITest(ApiTest):
    API_TOKEN = None

    def setUp(self):
        super(ContactAPITest, self).setUp()
        AccessGroup(name="OMAD", access_group_id="u_astra_group1").save()
        user = User.objects.create_user(username='testuser', password='12345')
        token = Token.objects.create(user=user)
        self.API_TOKEN = token.key

    def test_api_auth(self):
        test_request = {
            "adviser_netid": "javerage",
            "student_systemkey": "12345",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass"
        }

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        response = self.post_response('contact_omad',
                                      test_request)
        self.assertEqual(response.status_code, 201)
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION="BAD TOKEN")

        response = self.post_response('contact_omad',
                                      test_request)
        self.assertEqual(response.status_code, 401)

    @patch('compass.views.api.contact.Student')
    @patch('compass.views.api.contact.AppUser')
    @patch('compass.views.api.contact.Contact')
    @patch('compass.views.api.contact.AccessGroup')
    def test_post(self, mock_access_group_cls, mock_contact_cls,
                  mock_appuser_cls, mock_student_cls):
        mock_omad_access_group = MagicMock()
        mock_access_group_cls.objects.by_name = MagicMock(
            return_value=mock_omad_access_group)
        mock_view = ContactOMADView()
        # mock parsing/validation methods
        mock_view.validate_adviser_netid = MagicMock()
        mock_view.validate_student_systemkey = MagicMock()
        mock_parsed_checkin_date = MagicMock()
        mock_view.parse_checkin_date_str = \
            MagicMock(return_value=mock_parsed_checkin_date)
        mock_parsed_contact_date = MagicMock()
        mock_view.parse_contact_type_str = \
            MagicMock(return_value=mock_parsed_contact_date)
        # mock getting app user and student record
        mock_appuser = MagicMock()
        mock_appuser_cls.objects.upsert_appuser = \
            MagicMock(return_value=mock_appuser)
        mock_student = MagicMock()
        mock_student_cls.objects.get_or_create.return_value = \
            (mock_student, None)
        # mock saving contact
        mock_contact = mock_contact_cls()
        mock_contact.save = MagicMock()
        mock_contact.access_group.add = MagicMock()

        # assertions
        mock_request = MagicMock()
        response = mock_view.post(mock_request)
        mock_access_group_cls.objects.by_name.assert_called_once_with("OMAD")
        # assert parsing and validating contact
        mock_view.validate_adviser_netid.assert_called_once_with(
            mock_request.data.get("adviser_netid"))
        mock_view.validate_student_systemkey.assert_called_once_with(
            mock_request.data.get("student_systemkey"))
        mock_view.parse_checkin_date_str.assert_called_once_with(
            mock_request.data.get("checkin_date"))
        mock_view.parse_contact_type_str.assert_called_once_with(
            mock_request.data.get("contact_type"), mock_omad_access_group)
        # assert creating student record and app user record
        mock_appuser_cls.objects.upsert_appuser.assert_called_once_with(
            mock_request.data["adviser_netid"])
        mock_student_cls.objects.get_or_create.assert_called_once()
        # assert creating contact record
        self.assertEqual(mock_contact.app_user, mock_appuser)
        self.assertEqual(mock_contact.student, mock_student)
        self.assertEqual(mock_contact.contact_type,
                         mock_request.data["contact_type"])
        self.assertEqual(mock_contact.checkin_date,
                         mock_request.data["checkin_date"])
        mock_contact.save.assert_called_once()
        mock_contact.access_group.add.assert_called_once_with(
            mock_omad_access_group)
        self.assertEqual(response.status_code, 201)

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

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        # create without padding
        self.post_response('contact_omad',
                           test_nopad)
        call_command('process_omad_contacts')
        contacts = Contact.objects.all()
        self.assertEqual(contacts[0].student.system_key, "001234567")

        # create with padding
        self.post_response('contact_omad',
                           test_pad)
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

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        self.post_response('contact_omad',
                           test_noid)
        self.post_response('contact_omad',
                           test_id)
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

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        self.post_response('contact_omad',
                           test_id)
        call_command('process_omad_contacts')
        contacts = Contact.objects.all()

        c_id = contacts[0].id
        self.delete_response('contact_edit_view', 'javerage', contactid=c_id)

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

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        resp = self.post_response('contact_omad',
                                  test_checkin)
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
                              contactid=1)
        self.assertEqual(r.status_code, 200)
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.notes, "test note")
        self.assertEqual(contact.app_user.uwnetid, "javerage")

        r = self.put_response('contact_edit_view',
                              "javerage",
                              put_body,
                              contactid=1)
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
                               post_body,
                               netid="javerage")
        contacts = Contact.objects.all()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(contacts[0].notes, "test")
