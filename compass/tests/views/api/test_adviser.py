# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import override_settings
from unittest.mock import patch
from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, AppUser, Student, ContactType
from datetime import datetime, timezone
import json


class AdviserCheckInsAPITest(ApiTest):

    def test_get(self):
        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"},
                                     get_args={"days": "3"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data, {
            "adviser": {
                "id": 4, "uwnetid": "jadviser",
                "uwregid": "5136CCB9F66711D5BE060004AC494FF0",
                "pronouns": "He/him/his", "full_name": "Jay Adviser",
                "display_name": "Jay Adviser", "first_name": "Jay",
                "surname": "Adviser", "preferred_first_name": None,
                "preferred_middle_name": None, "preferred_surname": None,
                "whitepages_publish": False, "is_active_student": False,
                "is_active_employee": True, "last_changed": None,
                "system_key": None, "prior_uwnetids": ["jadviser1"],
                "prior_uwregids": [],
            },
            "contacts": []
        })

        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "1a1a1a1"},
                                     get_args={"days": "3"})
        self.assertEqual(response.status_code, 400, "Invalid uwnetid")

        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser2"},
                                     get_args={"days": "3"})
        self.assertEqual(response.status_code, 404, "Not found uwnetid")

    @patch("compass.views.api.adviser.Contact")
    def test_days_param(self, mock_contact_cls):
        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"},
                                     get_args={"days": "14"})
        mock_contact_cls.objects.by_adviser.assert_called_with(
            "jadviser", from_days=14)

        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"},
                                     get_args={"days": ""})
        mock_contact_cls.objects.by_adviser.assert_called_with(
            "jadviser", from_days=3)

        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"},
                                     get_args={"days": "seven"})
        mock_contact_cls.objects.by_adviser.assert_called_with(
            "jadviser", from_days=3)

        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"},
                                     get_args={"days": "2"})
        mock_contact_cls.objects.by_adviser.assert_called_with(
            "jadviser", from_days=3)

        response = self.get_response("adviser_checkins",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"},
                                     get_args={"days": "92"})
        mock_contact_cls.objects.by_adviser.assert_called_with(
            "jadviser", from_days=3)


class AdviserCaseloadAPITest(ApiTest):
    def test_get(self):
        response = self.get_response("adviser_caseload",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data["adviser"], {
            "id": 4, "uwnetid": "jadviser",
            "uwregid": "5136CCB9F66711D5BE060004AC494FF0",
            "pronouns": "He/him/his", "full_name": "Jay Adviser",
            "display_name": "Jay Adviser", "first_name": "Jay",
            "surname": "Adviser", "preferred_first_name": None,
            "preferred_middle_name": None, "preferred_surname": None,
            "whitepages_publish": False, "is_active_student": False,
            "is_active_employee": True, "last_changed": None,
            "system_key": None, "prior_uwnetids": ["jadviser1"],
            "prior_uwregids": []
        })
        self.assertEqual(len(response.data["caseload"]), 3)

        response = self.get_response("adviser_caseload",
                                     "jadviser",
                                     kwargs={"adviser_netid": "1a1a1a1"})
        self.assertEqual(response.status_code, 400, "Invalid uwnetid")

        response = self.get_response("adviser_caseload",
                                     "jadviser",
                                     kwargs={"adviser_netid": "jadviser2"})
        self.assertEqual(response.status_code, 404, "Not found uwnetid")


class ContactAPITest(ApiTest):
    ag = None
    app_user = None
    student = None
    contact_type = None

    def setUp(self):
        super(ContactAPITest, self).setUp()
        self.ag = AccessGroup(name="Test OMAD Group",
                              access_group_id="u_astra_group1")
        self.ag.save()
        self.app_user = AppUser(uwnetid="javerage")
        self.app_user.save()
        self.student = Student(system_key="532353230")
        self.student.save()
        self.contact_type = ContactType(access_group=self.ag,
                                        name="contact",
                                        slug="contact")
        self.contact_type.save()

    @override_settings(CURRENT_DATETIME_OVERRIDE="2013-05-10 12:00:01")
    def test_get_contacts(self):
        d1 = datetime(2013, 5, 10, 2, 30, 30, 300, tzinfo=timezone.utc)
        d2 = datetime(2013, 5, 7, 12, 1, 30, 300, tzinfo=timezone.utc)
        d3 = datetime(2013, 5, 4, 9, 0, 00, 100, tzinfo=timezone.utc)

        for date in [d1, d2, d3]:
            contact = Contact(app_user=self.app_user,
                              student=self.student,
                              checkin_date=date,
                              contact_type=self.contact_type,
                              source="Checkin")
            contact.save()
            contact.access_group.add(self.ag)

        # Don't display manual contacts
        contact = Contact(app_user=self.app_user,
                          student=self.student,
                          checkin_date=d2,
                          contact_type=self.contact_type,
                          source="Compass")
        contact.save()
        contact.access_group.add(self.ag)

        resp = self.get_response("adviser_checkins",
                                 "javerage",
                                 args=["javerage"])
        response = json.loads(resp.content)
        self.assertEqual(len(response), 2)
