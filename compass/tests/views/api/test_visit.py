# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import UTC, datetime
from django.test import Client
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from compass.views.api.visit import VisitOMADView
from compass.tests import ApiTest
from compass.models import (AccessGroup,
                            VisitType,
                            Visit,
                            Student,
                            VisitTutoringOption)
from rest_framework.authtoken.models import Token


class VisitAPITest(ApiTest):
    API_TOKEN = None

    def setUp(self):
        super(VisitAPITest, self).setUp()
        user = User.objects.create_user(username='testuser', password='12345')
        ag = AccessGroup(name="OMAD", access_group_id="u_astra_group1")
        ag.save()
        v_type = VisitType(name="IC Drop-In Tutoring", access_group=ag)
        v_type.save()
        v_tutoring = VisitTutoringOption(
            name="Option 1", access_group=ag)
        v_tutoring.save()
        stu = Student(system_key="888777333")
        stu.save()
        Visit(student=stu,
              access_group=ag,
              visit_type=v_type,
              course_code="CHEM 198",
              checkin_date=datetime(2022, 9, 19, 6, 15, 4, tzinfo=UTC),
              checkout_date=datetime(2022, 9, 19, 7, 15, 4, tzinfo=UTC),
              tutoring_option=v_tutoring).save()

        token = Token.objects.create(user=user)
        self.API_TOKEN = token.key

    def test_api_auth(self):
        test_request = {
            "student_netid": "javerage",
            "visit_type": "IC Drop-In Tutoring",
            "course_code": "CHEM 198",
            "checkin_date": "2012-01-19 13:21:00 PDT",
            "checkout_date": "2012-01-19 14:52:00 PDT"
        }

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        response = self.post_response('visit_omad', body=test_request)
        self.assertEqual(response.status_code, 201)
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION="BAD TOKEN")

        response = self.post_response('visit_omad', test_request)
        self.assertEqual(response.status_code, 401)

    def test_date_parse(self):
        # no checkin date specified
        self.assertIsNone(VisitOMADView()._valid_date(None))

        # bad checkin format
        with self.assertRaises(ValueError):
            VisitOMADView()._valid_date("2022-09-T::")
        # Missing TZ info
        with self.assertRaises(ValueError):
            VisitOMADView()._valid_date("2022-09-19T06:15:04")
        # correct checkin format
        checkin_date = VisitOMADView()._valid_date("2022-09-19T06:15:04Z")
        self.assertEqual(type(checkin_date), datetime)

    def test_valid_student(self):
        with self.assertRaises(ValueError):
            VisitOMADView()._valid_student(None)

        with self.assertRaises(ValueError):
            VisitOMADView()._valid_student("badnetid")

        student = VisitOMADView()._valid_student("javerage")
        self.assertEqual(student.system_key, "532353230")

    @patch('compass.views.api.visit.Visit')
    @patch('compass.views.api.visit.VisitType')
    @patch('compass.views.api.visit.get_appuser_by_uwnetid')
    @patch('compass.views.api.visit.Student')
    @patch('compass.views.api.visit.AccessGroup')
    def test_post(self, mock_access_group_cls,
                  mock_student_cls,
                  mock_get_appuser_by_uwnetid,
                  mock_visit_type_cls,
                  mock_visit_cls):

        mock_omad_access_group = MagicMock()
        mock_access_group_cls.objects.by_name = MagicMock(
            return_value=mock_omad_access_group)

        mock_view = VisitOMADView()

        mock_student = MagicMock()
        mock_view._valid_student = MagicMock(
            return_value=mock_student)

        mock_visit_type = MagicMock()
        mock_visit_type_cls.objects.get.return_value = mock_visit_type

        mock_view._valid_visit_type = MagicMock(
            return_value=mock_visit_type)

        mock_course = MagicMock()
        mock_view._valid_course = MagicMock(
            return_value=mock_course)

        mock_date = MagicMock()
        mock_view._valid_date = MagicMock(
            return_value=mock_date)

        mock_visit_cls.return_value = (mock_visit_cls, None)
        mock_visit_cls.objects.update_or_create = mock_visit_cls

        # assertions
        mock_request = MagicMock()
        response = mock_view.post(mock_request)
        mock_access_group_cls.objects.by_name.assert_called_once_with("OMAD")

        # assert parsing and validating visit
        mock_view._valid_student.assert_called_once_with(
            mock_request.data.get("student_netid"))
        mock_view._valid_course.assert_called_once_with(
            mock_request.data.get("course_code"))
        mock_view._valid_date.assert_called_with(
            mock_request.data.get("checkin_date"))
        mock_view._valid_date.assert_called_with(
            mock_request.data.get("checkout_date"))
        mock_view._valid_visit_type.assert_called_once_with(
            mock_request.data.get("visit_type"), mock_omad_access_group)

        # assert visit record called correctly
        mock_visit_cls.assert_called_once_with(
            student=mock_student,
            access_group=mock_omad_access_group,
            course_code=mock_course,
            checkin_date=mock_date,
            defaults={
                'checkout_date': mock_date, 'visit_type': mock_visit_type})

        self.assertEqual(response.status_code, 201)

    def test_get_active_ic_visits(self):
        response = self.get_response('active_ic_visit_list', 'jadviser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pending_verification', response.data)
        self.assertIn('by_programarea', response.data)
        self.assertEqual(len(response.data['pending_verification']), 2)
        self.assertEqual(len(response.data['by_programarea']), 2)
        self.assertEqual(
            len(response.data['by_programarea']['Program Area 2']), 1)
        self.assertEqual(
            len(response.data['by_programarea']['Program Area 3']), 2)

    def test_student_visit_search(self):
        response = self.get_response('visit_search_view',
                                     "jadviser",
                                     kwargs={"identifier": "lisa"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['student'], 1)
        self.assertEqual(response.data[0]['visit_type']['name'],
                         "IC Drop-In Tutoring")
        self.assertEqual(response.data[0]['course_code'], "CHEM 198")
        self.assertEqual(response.data[0]['tutoring_option']['name'],
                         "Option 1")
        self.assertEqual(response.data[0]['checkin_date'],
                         "2022-09-19T06:15:04Z")
        self.assertEqual(response.data[0]['checkout_date'],
                         "2022-09-19T07:15:04Z")

        no_person_resp = self.get_response('visit_search_view',
                                           "jadviser",
                                           kwargs={"identifier": "badnetid"})
        self.assertEqual(no_person_resp.status_code, 404)

        no_stu_resp = self.get_response('visit_search_view',
                                        "jadviser",
                                        kwargs={"identifier": "javerage"})
        self.assertEqual(no_stu_resp.status_code, 404)

        bad_identifier_resp = self.get_response('visit_search_view',
                                                "jadviser",
                                                kwargs={
                                                    "identifier": "1234bad"})
        self.assertEqual(bad_identifier_resp.status_code, 400)

        syskey_resp = self.get_response('visit_search_view',
                                        "jadviser",
                                        kwargs={"identifier": "1233338"})
        self.assertEqual(syskey_resp.status_code, 200)
        self.assertEqual(len(syskey_resp.data), 1)

    def test_get_ic_visit_options(self):
        response = self.get_response('ic_visit_options_view', "jadviser")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['program_areas']), 4)
        self.assertEqual(len(response.data['tutoring_options']), 3)
        self.assertEqual(len(response.data['writing_services']), 2)
