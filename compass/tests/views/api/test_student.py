# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, ContactType, Student
from uw_pws.util import fdao_pws_override
from uw_sws.util import fdao_sws_override


class StudentAPITest(ApiTest):
    def test_get_student(self):
        response = self.get_response("student_view",
                                     "jadvisor",
                                     None,
                                     kwargs={"identifier": "javerage"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uwnetid"], "javerage")
        self.assertEqual(len(response.data["photo_url"]), 70)
        self.assertEqual(response.data["analytics_alert"], "success")

        response = self.get_response("student_view",
                                     "jadvisor",
                                     None,
                                     kwargs={"identifier": "nobody"})
        self.assertEqual(response.status_code, 404)


class StudentSearchAPITest(ApiTest):
    def test_get_search(self):
        response = self.get_response("student_search_view",
                                     "jadvisor",
                                     {"query": "javerage"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uwnetid"], "javerage")

        response = self.get_response("student_search_view",
                                     "jadvisor",
                                     {"query": "nobody"})
        self.assertEqual(response.status_code, 404)


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
        response = self.get_response("student_contacts_view",
                                     "javerage",
                                     None,
                                     kwargs={"systemkey": "000000067"})

        # Ensure greedy matching not occuring per CMPS-187
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.get_response("student_contacts_view",
                                     "javerage",
                                     None,
                                     kwargs={"systemkey": "0011111"})
        self.assertEqual(response.status_code, 400)


class StudentAffiliationsAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="OMAD", access_group_id="u_astra_group1-manager")

    def test_get_affiliations(self):
        response = self.get_response("student_affiliations_view",
                                     "jadviser",
                                     None,
                                     kwargs={"systemkey": "532353230"})

        self.assertEqual(response.status_code, 401)


@fdao_pws_override
@fdao_sws_override
class StudentTranscriptsAPITest(ApiTest):
    def test_get_transcripts(self):
        response = self.get_response(
            "student_transcripts_view", "jadvisor", None,
            kwargs={"uwregid": "9136CCB8F66711D5BE060004AC494FFE"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = self.get_response(
            "student_transcripts_view", "jadvisor", None,
            kwargs={"uwregid": "7776CCB8F66711D5BE060004AC494AAA"})
        self.assertEqual(response.status_code, 404)


class StudentSchedulesAPITest(ApiTest):
    def test_get_schedules(self):
        response = self.get_response(
            "student_schedules_view", "jadvisor", None,
            kwargs={"uwregid": "9136CCB8F66711D5BE060004AC494FFE"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.get_response(
            "student_schedules_view", "jadvisor", None,
            kwargs={"uwregid": "7776CCB8F66711D5BE060004AC494AAA"})
        self.assertEqual(response.status_code, 404)
