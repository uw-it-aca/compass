# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from datetime import datetime, timezone
from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, AppUser, Student, ContactType
from freezegun import freeze_time


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
        self.student = Student(system_key="12345")
        self.student.save()
        self.contact_type = ContactType(access_group=self.ag,
                                        name="contact",
                                        slug="contact")
        self.contact_type.save()

    @freeze_time("2023-05-10  12:00:01", tz_offset=0)
    def test_get_contacts(self):
        d1 = datetime(2023, 5, 10, 2, 30, 30, 300, tzinfo=timezone.utc)
        d2 = datetime(2023, 5, 7, 12, 1, 30, 300, tzinfo=timezone.utc)
        d3 = datetime(2023, 5, 7, 12, 0, 00, 100, tzinfo=timezone.utc)

        for date in [d1, d2, d3]:
            contact = Contact(app_user=self.app_user,
                              student=self.student,
                              checkin_date=date,
                              contact_type=self.contact_type)
            contact.save()
            contact.access_group.add(self.ag)

        resp = self.get_response("adviser_contacts",
                                 "javerage",
                                 args=["javerage"])
        response = json.loads(resp.content)

        self.assertEqual(len(response), 2)
