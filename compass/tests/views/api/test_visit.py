# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from django.test import Client
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from compass.views.api.visit import VisitOMADView
from compass.tests import ApiTest
from compass.models import AccessGroup, VisitType
from rest_framework.authtoken.models import Token


class ViewAPITest(ApiTest):
    API_TOKEN = None

    def setUp(self):
        super(ViewAPITest, self).setUp()
        user = User.objects.create_user(username='testuser', password='12345')
        ag = AccessGroup(name="OMAD", access_group_id="u_astra_group1")
        ag.save()
        VisitType(name="IC Drop-In Tutoring", access_group=ag).save()
        token = Token.objects.create(user=user)
        self.API_TOKEN = token.key

    def test_api_auth(self):
        test_request = {
            "student_netid": "javerage",
            "visit_type": "ic-drop-in-tutoring",
            "course_code": "CHEM 198",
            "checkin_date": "2012-01-19 13:21:00 PDT",
            "checkout_date": "2012-01-19 14:52:00 PDT"
        }

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        response = self.post_response('visit_omad', test_request)
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
    @patch('compass.views.api.visit.UWPersonClient')
    @patch('compass.views.api.visit.Student')
    @patch('compass.views.api.visit.AccessGroup')
    def test_post(self, mock_access_group_cls,
                  mock_student_cls,
                  mock_person_client_cls,
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
        mock_visit_type_cls.objects.get.return_value = \
            mock_visit_type

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
