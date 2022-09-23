# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch
from compass.views.api.contact import ContactOMADView


class ContactAPITest(TestCase):

    def test_parse_checkin_date_str(self):
        # no checkin date specified
        with self.assertRaises(ValueError):
            ContactOMADView().parse_checkin_date_str(None)
        # bad checkin format
        with self.assertRaises(ValueError):
            ContactOMADView().parse_checkin_date_str("2022-09-T::")
        # correct checkin format
        checkin_date = ContactOMADView().parse_checkin_date_str(
            "2022-09-19T06:15:04Z")
        self.assertEqual(type(checkin_date), datetime)

    def test_validate_adviser_netid(self):
        with self.assertRaises(ValueError):
            ContactOMADView().validate_adviser_netid(None)
        ContactOMADView().validate_adviser_netid("foo")

    def test_validate_student_systemkey(self):
        with self.assertRaises(ValueError):
            ContactOMADView().validate_student_systemkey(None)
        with self.assertRaises(ValueError):
            ContactOMADView().validate_student_systemkey("badsyskey")
        ContactOMADView().validate_adviser_netid("1234")

    @patch('compass.views.api.contact.settings')
    @patch('compass.views.api.contact.AccessGroup')
    def test_post_not_omad_group_member(
            self, mock_access_group, mock_settings):
        mock_omad_access_group = MagicMock()
        mock_access_group.objects.get = \
            MagicMock(return_value=mock_omad_access_group)
        mock_access_group.objects.is_access_group_member = \
            MagicMock(return_value=False)
        response = ContactOMADView().post(MagicMock())
        self.assertEqual(response.status_code, 400)

    @patch('compass.views.api.contact.Student')
    @patch('compass.views.api.contact.AppUser')
    @patch('compass.views.api.contact.Contact')
    @patch('compass.views.api.contact.AccessGroup')
    @patch('compass.views.api.contact.settings')
    def test_post(
            self, mock_settings, mock_access_group_cls,
            mock_contact_cls, mock_appuser_cls, mock_student_cls):
        mock_omad_access_group = MagicMock()
        mock_access_group_cls.objects.get = \
            MagicMock(return_value=mock_omad_access_group)
        mock_access_group_cls.objects.is_access_group_member.return_value = \
            True
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
        mock_access_group_cls.objects.get.assert_called_once_with(
            access_group_id=mock_settings.OMAD_ACCESS_GROUP_ID)
        mock_access_group_cls.objects.is_access_group_member.\
            assert_called_once_with(mock_request.data["adviser_netid"],
                                    mock_omad_access_group)
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
        mock_student_cls.objects.get_or_create.assert_called_once_with(
            system_key=mock_request.data["student_systemkey"])
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
