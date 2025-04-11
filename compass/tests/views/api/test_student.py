# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, ContactType, Student
from uw_pws.util import fdao_pws_override
from uw_sws.util import fdao_sws_override


class StudentContactAPITest(ApiTest):
    def setUp(self):
        super().setUp()
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


@fdao_pws_override
@fdao_sws_override
class StudentTranscriptsAPITest(ApiTest):
    def test_get_transcripts(self):
        transcripts = self.get_response(
            "student_transcripts_view", "jadvisor", None,
            kwargs={"uwregid": "9136CCB8F66711D5BE060004AC494FFE"})

        self.assertEqual(len(transcripts.data), 3)
