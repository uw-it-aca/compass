# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import CompassTestCase
from compass.models import AppUser, Contact, Student, AccessGroup, ContactType
from datetime import datetime, timezone


class AppUserTest(CompassTestCase):
    def test_upsert_create(self):
        user = AppUser.objects.upsert_appuser("javerage")
        self.assertEqual(user.uwnetid, "javerage")
        self.assertEqual(user.display_name, "Jamesy McJamesy")
        self.assertEqual(len(AppUser.objects.filter(uwnetid="javerage")), 1)

    def test_upsert_update(self):
        AppUser(uwnetid="jadviser1").save()
        user = AppUser.objects.upsert_appuser("jadviser")
        self.assertEqual(user.uwnetid, "jadviser")
        self.assertEqual(user.display_name, "Jay Adviser")
        self.assertEqual(len(AppUser.objects.filter(uwnetid="jadviser")), 1)
        self.assertRaises(AppUser.DoesNotExist,
                          AppUser.objects.get,
                          uwnetid="jadviser1")

    def test_upsert_duplicate(self):
        ag = AccessGroup(name="Test OMAD Group",
                         access_group_id="u_astra_group1")
        ag.save()
        prior_user = AppUser(uwnetid="jadviser1")
        prior_user.save()
        curr_user = AppUser(uwnetid="jadviser")
        curr_user.save()
        student = Student(system_key="532353230")
        student.save()
        contact_type = ContactType(access_group=ag,
                                   name="contact",
                                   slug="contact")
        contact_type.save()

        contact1 = Contact(app_user=prior_user,
                           student=student,
                           checkin_date=datetime(2023, 5, 10, 2, 30, 30, 300,
                                                 tzinfo=timezone.utc),
                           contact_type=contact_type)
        contact1.save()
        contact2 = Contact(app_user=curr_user,
                           student=student,
                           checkin_date=datetime(2023, 5, 10, 2, 30, 30, 300,
                                                 tzinfo=timezone.utc),
                           contact_type=contact_type)
        contact2.save()
        self.assertEqual(len(Contact.objects.filter(app_user=prior_user)), 1)
        self.assertEqual(len(Contact.objects.filter(app_user=curr_user)), 1)

        AppUser.objects.upsert_appuser("jadviser")
        self.assertEqual(len(Contact.objects.filter(app_user=prior_user)), 0)
        self.assertEqual(len(Contact.objects.filter(app_user=curr_user)), 2)
