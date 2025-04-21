# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, ContactType, Student
from uw_pws.util import fdao_pws_override
from uw_sws.util import fdao_sws_override
from mock import patch
import json


class StudentAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        self.ag = AccessGroup(name="Test Group",
                              access_group_id="u_astra_group1")
        self.ag.save()

    def test_get(self):
        response = self.get_response("student_view",
                                     "jadviser",
                                     kwargs={"identifier": "javerage"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data["uwnetid"], "javerage")
        self.assertEqual(len(response.data["photo_url"]), 70)
        self.assertEqual(response.data["analytics_alert"], "success")

        response = self.get_response("student_view",
                                     "jadviser",
                                     kwargs={"identifier": "nobody"})
        self.assertEqual(response.status_code, 404, "Student not found")

        response = self.get_response("student_view",
                                     "jadviser",
                                     kwargs={"identifier": "1033334"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data["uwnetid"], "javerage")
        self.assertEqual(len(response.data["photo_url"]), 70)
        self.assertEqual(response.data["analytics_alert"], "success")

        response = self.get_response("student_view",
                                     "jadviser",
                                     kwargs={"identifier": "7777777"})
        self.assertEqual(response.status_code, 404, "Student not found")

        response = self.get_response("student_view",
                                     "jadviser",
                                     kwargs={"identifier": "1a2b3c4"})
        self.assertEqual(response.status_code, 400, "Invalid identifier")

    @patch('compass.dao.group.is_member_of_group')
    def test_post(self, mock_is_member):
        mock_is_member.return_value = True
        post_body = json.dumps({
            "system_key": "532353230", "programs": ["ABC"]})

        response = self.post_response("student_view",
                                      netid="jadviser",
                                      kwargs={"identifier": "jbothell"})
        self.assertEqual(response.status_code, 400, "Missing POST body")

        mock_is_member.return_value = False
        post_body = json.dumps({
            "system_key": "532353230", "programs": ["ABC"]})

        response = self.post_response("student_view",
                                      netid="jadviser",
                                      body=post_body,
                                      kwargs={"identifier": "jbothell"})
        self.assertEqual(response.status_code, 401, "Unauthorized")


class StudentSearchAPITest(ApiTest):
    def test_get(self):
        response = self.get_response("student_search_view",
                                     "jadviser",
                                     get_args={"query": "javerage"})

        self.assertEqual(response.status_code, 200, "OK UWnetid")
        self.assertEqual(response.data["uwnetid"], "javerage")

        response = self.get_response("student_search_view",
                                     "jadviser",
                                     get_args={"query": "nobody"})
        self.assertEqual(response.status_code, 404, "UWnetid not found")

        response = self.get_response("student_search_view",
                                     "jadviser",
                                     get_args={"query": "1033334"})

        self.assertEqual(response.status_code, 200, "OK student number")
        self.assertEqual(response.data["uwnetid"], "javerage")

        response = self.get_response("student_search_view",
                                     "jadviser",
                                     get_args={"query": "7777777"})
        self.assertEqual(response.status_code, 404, "Student num not found")

        response = self.get_response("student_search_view",
                                     "jadviser",
                                     get_args={"query": "1"})
        self.assertEqual(response.status_code, 400, "Invalid query")


class StudentContactsAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(name="Test Group",
                                        access_group_id="u_astra_group1")

        stu1 = Student.objects.create(system_key="001234567")
        stu2 = Student.objects.create(system_key="000000067")
        ct = ContactType.objects.create(access_group=ag, name="foo")
        Contact.objects.create(student=stu1, contact_type=ct,
                               checkin_date="2022-09-19T06:15:04Z")
        Contact.objects.create(student=stu2, contact_type=ct,
                               checkin_date="2022-09-19T06:15:04Z")

    def test_get(self):
        response = self.get_response("student_contacts_view",
                                     "jadviser",
                                     kwargs={"systemkey": "000000067"})

        # Ensure greedy matching not occuring per CMPS-187
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(len(response.data), 1)

        response = self.get_response("student_contacts_view",
                                     "javerage",
                                     kwargs={"systemkey": "0011111"})
        self.assertEqual(response.status_code, 400, "Invalid system key")


class StudentVisitsAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="Test Group", access_group_id="u_astra_group1")

    @patch('compass.dao.group.is_member_of_group')
    def test_get(self, mock_is_member):
        mock_is_member.return_value = True
        response = self.get_response("student_visits_view",
                                     "jadviser",
                                     kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(len(response.data), 0)

        mock_is_member.return_value = False
        response = self.get_response("student_visits_view",
                                     "jadviser",
                                     kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 401, "Unauthorized")


class StudentAffiliationsAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="Test Group", access_group_id="u_astra_group1")

    @patch('compass.dao.group.is_member_of_group')
    def test_get(self, mock_is_member):
        mock_is_member.return_value = True
        response = self.get_response("student_affiliations_view",
                                     "jadviser",
                                     kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data, [])

        mock_is_member.return_value = False
        response = self.get_response("student_affiliations_view",
                                     "jadviser",
                                     kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

    @patch('compass.dao.group.is_member_of_group')
    def test_post(self, mock_is_member):
        mock_is_member.return_value = True
        response = self.post_response("student_affiliations_view",
                                      "jadviser",
                                      kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 404, "Student not found")

        mock_is_member.return_value = False
        response = self.post_response("student_affiliations_view",
                                      "jadviser",
                                      kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

    @patch('compass.dao.group.is_member_of_group')
    def test_delete(self, mock_is_member):
        mock_is_member.return_value = True

        response = self.delete_response(
            "student_affiliation_view", "jadviser", kwargs={
                "systemkey": "invalid", "affiliation_id": "1"})
        self.assertEqual(response.status_code, 400, "Invalid systemkey")

        response = self.delete_response(
            "student_affiliation_view", "jadviser", kwargs={
                "systemkey": "532353230", "affiliation_id": "1"})
        self.assertEqual(response.status_code, 404, "Affiliation not found")

        mock_is_member.return_value = False
        response = self.delete_response(
            "student_affiliation_view", "jadviser", kwargs={
                "systemkey": "532353230", "affiliation_id": "1"})
        self.assertEqual(response.status_code, 401, "Unauthorized")


class StudentAffiliationsImportAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="Test Group", access_group_id="u_astra_group1")

    @patch('compass.dao.group.is_member_of_group')
    def test_post(self, mock_is_member):
        mock_is_member.return_value = False
        response = self.post_response("student_affiliations_import_view",
                                      "jadviser",
                                      kwargs={"affiliation_id": "1"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

        mock_is_member.return_value = True
        response = self.post_response("student_affiliations_import_view",
                                      "jadviser",
                                      kwargs={"affiliation_id": "1"})
        self.assertEqual(response.status_code, 400, "Missing POST body")

        response = self.post_response("student_affiliations_import_view",
                                      "jadviser",
                                      body=json.dumps({"cohort": ""}),
                                      kwargs={"affiliation_id": "1"})
        self.assertEqual(response.status_code, 400, "Missing cohort")

        response = self.post_response("student_affiliations_import_view",
                                      "jadviser",
                                      body=json.dumps({"cohort": "2013"}),
                                      kwargs={"affiliation_id": "1"})
        self.assertEqual(response.status_code, 400, "Invalid cohort")

        response = self.post_response("student_affiliations_import_view",
                                      "jadviser",
                                      body=json.dumps({"cohort": "2013-2014"}),
                                      kwargs={"affiliation_id": "1"})
        self.assertEqual(response.status_code, 400, "Unknown cohort")


@fdao_pws_override
@fdao_sws_override
class StudentTranscriptsAPITest(ApiTest):
    def test_get(self):
        response = self.get_response(
            "student_transcripts_view", "jadviser",
            kwargs={"uwregid": "9136CCB8F66711D5BE060004AC494FFE"})

        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(len(response.data), 3)

        response = self.get_response(
            "student_transcripts_view", "jadviser",
            kwargs={"uwregid": "7776CCB8F66711D5BE060004AC494AAA"})
        self.assertEqual(response.status_code, 404, "UWregid not found")


class StudentEligibilityAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="Test Group", access_group_id="u_astra_group1")

    @patch('compass.dao.group.is_member_of_group')
    def test_get(self, mock_is_member):
        mock_is_member.return_value = False
        response = self.get_response(
            "student_eligibility_view", "jadviser",
            kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

        mock_is_member.return_value = True
        response = self.get_response(
            "student_eligibility_view", "jadviser",
            kwargs={"systemkey": "invalid"})
        self.assertEqual(response.status_code, 400, "Invalid systemkey")

        response = self.get_response(
            "student_eligibility_view", "jadviser",
            kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data, [], "Empty list")

    @patch('compass.dao.group.is_member_of_group')
    def test_post(self, mock_is_member):
        post_body = json.dumps({"eligibility_type_id": "2"})

        mock_is_member.return_value = False
        response = self.post_response(
            "student_eligibility_view", "jadviser",
            body=post_body,
            kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

        mock_is_member.return_value = True
        response = self.post_response(
            "student_eligibility_view", "jadviser",
            body=post_body,
            kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 404, "Student not found")

        response = self.post_response(
            "student_eligibility_view", "jadviser",
            body=post_body,
            kwargs={"systemkey": "invalid"})
        self.assertEqual(response.status_code, 400, "Invalid systemkey")

        response = self.post_response(
            "student_eligibility_view", "jadviser",
            body=json.dumps({"eligibility_type_id": "-1"}),
            kwargs={"systemkey": "532353230"})
        self.assertEqual(response.status_code, 400, "Invalid eligibility type")


class StudentSchedulesAPITest(ApiTest):
    def test_get(self):
        response = self.get_response(
            "student_schedules_view", "jadviser",
            kwargs={"uwregid": "9136CCB8F66711D5BE060004AC494FFE"})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(len(response.data), 2)

        response = self.get_response(
            "student_schedules_view", "jadviser",
            kwargs={"uwregid": "7776CCB8F66711D5BE060004AC494AAA"})
        self.assertEqual(response.status_code, 404, "Not found")


class StudentCourseAnalyticsAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="Test Group", access_group_id="u_astra_group1")

    @patch('compass.dao.group.is_member_of_group')
    def test_get(self, mock_is_member):
        mock_is_member.return_value = False
        response = self.get_response(
            "student_course_analytics_view", "jadviser", kwargs={
                "year": 2023, "quarter": "autumn", "uwnetid": "javerage",
                "course_id": "test course"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

        mock_is_member.return_value = True
        response = self.get_response(
            "student_course_analytics_view", "jadviser", kwargs={
                "year": 2023, "quarter": "autumn", "uwnetid": "javerage",
                "course_id": "test course"})
        self.assertEqual(response.status_code, 404, "Not found")


class StudentSigninAnalyticsAPITest(ApiTest):
    def setUp(self):
        super().setUp()
        ag = AccessGroup.objects.create(
            name="Test Group", access_group_id="u_astra_group1")

    @patch('compass.dao.group.is_member_of_group')
    def test_get(self, mock_is_member):
        mock_is_member.return_value = False
        response = self.get_response(
            "student_signin_analytics_view", "jadviser",
            kwargs={"uwnetid": "javerage"})
        self.assertEqual(response.status_code, 401, "Unauthorized")

        mock_is_member.return_value = True
        response = self.get_response(
            "student_signin_analytics_view", "jadviser",
            kwargs={"uwnetid": "javerage"})
        self.assertEqual(response.status_code, 404, "Not found")
