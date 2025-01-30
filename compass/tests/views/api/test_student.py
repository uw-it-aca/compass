# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, ContactType, Student


class StudentContactAPITest(ApiTest):
    def setUp(self):
        super(StudentContactAPITest, self).setUp()
        ag = AccessGroup.objects.create(name="OMAD",
                                        access_group_id="u_astra_group1")

        stu1 = Student.objects.create(system_key="001234567")
        stu2 = Student.objects.create(system_key="000000067")
        ct = ContactType.objects.create(access_group=ag, name="foo")
        Contact.objects.create(student=stu1, contact_type=ct,
                               checkin_date="2022-09-19T06:15:04Z")
        Contact.objects.create(student=stu2, contact_type=ct,
                               checkin_date="2022-09-19T06:15:04Z")

    def test_get_contacts(self):
        contacts = self.get_response("student_contacts_view",
                                     "javerage",
                                     None,
                                     kwargs={"systemkey": "000000067"})

        # Ensure greedy matching not occuring per CMPS-187
        self.assertEqual(len(contacts.data), 1)
