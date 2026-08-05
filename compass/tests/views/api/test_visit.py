# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import UTC, datetime
from unittest.mock import MagicMock, call, patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from rest_framework.authtoken.models import Token
from restclients_core.exceptions import DataFailureException

from compass.dao.person import PersonNotFoundException
from compass.models import (
    AccessGroup,
    Student,
    Visit,
    VisitTutoringOption,
    VisitType,
)
from compass.tests import ApiTest
from compass.views.api.visit import VisitOMADView, VisitSearchMixin


class VisitAPITest(ApiTest):
    API_TOKEN = None
    ACCESS_GROUP = None

    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username='compass-visits-api',
                                        password='12345')
        ag = AccessGroup(name="OMAD", access_group_id="u_astra_group1")
        ag.save()
        self.ACCESS_GROUP = ag
        v_type = VisitType(name="IC Drop-In Tutoring", access_group=ag)
        v_type.save()
        v_tutoring = VisitTutoringOption(
            name="Option 1", access_group=ag)
        v_tutoring.save()
        stu = Student(system_key="888777333")
        stu.save()
        stu2 = Student(system_key="532353230")
        stu2.save()
        Visit(student=stu,
              access_group=ag,
              visit_type=v_type,
              course_code="CHEM 198",
              checkin_date=datetime(2022, 9, 19, 6, 15, 4, tzinfo=UTC),
              checkout_date=datetime(2022, 9, 19, 7, 15, 4, tzinfo=UTC),
              tutoring_option=v_tutoring).save()
        Visit(student=stu2,
              access_group=ag,
              visit_type=v_type,
              course_code="MATH 124",
              checkin_date=datetime(2022, 9, 20, 6, 15, 4, tzinfo=UTC),
              checkout_date=datetime(2022, 9, 20, 7, 15, 4, tzinfo=UTC),
              tutoring_option=v_tutoring).save()

        token = Token.objects.create(user=user)
        self.API_TOKEN = token.key

    def test_api_auth(self):
        test_request = {
            "student_netid": "javerage",
            "visit_type": "IC Drop-In Tutoring", "course_code": "CHEM 198",
            "checkin_date": "2012-01-19 13:21:00 PDT",
            "checkout_date": "2012-01-19 14:52:00 PDT"
        }

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        response = self.post_response('visit_omad', body=test_request)
        self.assertEqual(response.status_code, 201)
        search_resp = self.get_response('external_student_visit_view',
                                        kwargs={"identifier": "javerage"})
        self.assertEqual(search_resp.status_code, 200)

        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION="BAD TOKEN")

        response = self.post_response('visit_omad', test_request)
        self.assertEqual(response.status_code, 401)
        search_resp = self.get_response('external_student_visit_view',
                                        kwargs={"identifier": "javerage"})
        self.assertEqual(search_resp.status_code, 401)

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

    def test_valid_tutoring_option(self):
        vto = VisitOMADView()._valid_tutoring_option("Option 1",
                                                     self.ACCESS_GROUP)
        self.assertEqual(vto.name, "Option 1")

        with self.assertRaises(ValueError):
            VisitOMADView()._valid_tutoring_option("Nonexistent Option",
                                                   self.ACCESS_GROUP)

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

        mock_tutoring_option = MagicMock()
        mock_view._valid_tutoring_option = MagicMock(
            return_value=mock_tutoring_option)

        mock_date = MagicMock()
        mock_view._valid_date = MagicMock(
            return_value=mock_date)

        mock_visit_cls.return_value = (mock_visit_cls, None)
        mock_visit_cls.objects.update_or_create = mock_visit_cls

        # assertions
        mock_request = MagicMock()
        mock_request.user.username = 'compass-visits-api'

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
        mock_view._valid_tutoring_option.assert_called_once_with(
            mock_request.data.get("tutoring_option"), mock_omad_access_group)

        # assert visit record called correctly
        mock_visit_cls.assert_called_once_with(
            student=mock_student,
            access_group=mock_omad_access_group,
            course_code=mock_course,
            checkin_date=mock_date,
            defaults={
                'checkout_date': mock_date,
                'visit_type': mock_visit_type,
                'tutoring_option': mock_tutoring_option})

        self.assertEqual(response.status_code, 201)

    def test_get_active_ic_visits(self):
        response = self.get_response('active_ic_visit_list', 'jadviser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pending_verification', response.data)
        self.assertIn('by_programarea', response.data)
        self.assertEqual(len(response.data['pending_verification']), 7)
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
                                        kwargs={"identifier": "jnewstudent"})

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
        param = {
            "uwregid": "9136CCB8F66711D5BE060004AC494FFE"
        }
        response = self.get_response('ic_visit_options_view',
                                     "jadviser",
                                     kwargs=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['program_areas']), 4)
        self.assertEqual(len(response.data['tutoring_options']), 3)
        self.assertEqual(len(response.data['writing_services']), 2)

    @patch('compass.dao.compass_visits.CompassVisits.get_visit_options')
    def test_get_ic_visit_options_datafailure(self, mock_get_visit_options):
        mock_get_visit_options.side_effect = DataFailureException(
            'compass-visits', 404, 'Not Found')

        response = self.get_response(
            'ic_visit_options_view',
            'jadviser',
            kwargs={"uwregid": "BADREGID"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['program_areas'], [])
        self.assertEqual(response.data['tutoring_options'], [])
        self.assertEqual(response.data['writing_services'], [])
        self.assertEqual(response.data['courses'], [])

    @patch('uw_compass_visits.CompassVisits.admin_create_visit')
    def test_create_visit(self, mock_admin_create_visit):
        from compass.dao import compass_visits
        data = {
            "student_syskey": "000043870",
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        compass_visits.admin_create_visit(data)
        # Check the Visit object passed to CompassVisits.admin_create_visit
        args, _kwargs = mock_admin_create_visit.call_args
        visit_arg = args[0]
        assert visit_arg.student_syskey == data["student_syskey"]
        assert visit_arg.program_area == data["program_area"]
        assert visit_arg.tutoring_option == data["tutoring_option"]
        assert visit_arg.writing_service == data["writing_service"]
        # course is not in data, should be None
        assert getattr(visit_arg, "course", None) is None

    def test_update_visit(self):
        visit_id = 1
        update_param = {
            "is_verified": True,
            "is_checked_out": True
        }
        update_response = self.patch_response('ic_visit_update_view',
                                              "jadviser",
                                              body=update_param,
                                              kwargs={"visit_id": visit_id})
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['is_verified'], True)
        self.assertIsNotNone(update_response.data['check_out_date'])
        self.assertEqual(update_response.data['program_area'],
                         "Program Area 1")

    def test_delete_visit(self):
        delete_response = self.delete_response('ic_visit_update_view',
                                               "jadviser",
                                               kwargs={"visit_id": 1})
        self.assertEqual(delete_response.status_code, 204)

        delete_response = self.delete_response('ic_visit_update_view',
                                               "jadviser",
                                               kwargs={"visit_id": 99})
        self.assertEqual(delete_response.status_code, 404)

    def test_IC_visit_file_upload(self):
        # create a sample CSV file
        csv_content = "student_number,course_name,duration_minutes\n"
        csv_content += "1033334,CHEM 198,60\n"
        file = SimpleUploadedFile("visits.csv",
                                  csv_content.encode('utf-8'),
                                  content_type="text/csv")
        form_data = {
            "file": file,
            "visit_type": "IC Drop-In Tutoring",
            "tutoring_option": "Option 1",
            "date": "2022-09-19",
        }
        response = self.post_multipart_response('ic_visit_file_view',
                                                "jadviser",
                                                body=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count_created'], 1)
        file = SimpleUploadedFile("visits.csv",
                                  csv_content.encode('utf-8'),
                                  content_type="text/csv")

        bad_visit_type_response = self.post_multipart_response(
            'ic_visit_file_view',
            "jadviser",
            body={
                **form_data,
                "visit_type": "Nonexistent Visit Type",
                "file": file
            })
        self.assertEqual(bad_visit_type_response.status_code, 400)
        self.assertIn('does not exist for access group',
                      bad_visit_type_response.data)

    def test_IC_visit_file_upload_missing_file(self):
        response = self.post_multipart_response(
            'ic_visit_file_view',
            "jadviser",
            body={
                "visit_type": "IC Drop-In Tutoring",
                "tutoring_option": "Option 1",
                "date": "2022-09-19",
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'No file uploaded')

    @patch('compass.views.api.visit.validate_visit_upload_file')
    def test_IC_visit_file_upload_invalid_file(self,
                                               mock_validate_upload_file):
        mock_validate_upload_file.return_value = (False, 'Invalid file')

        file = SimpleUploadedFile("visits.csv",
                                  b"not,a,valid,file\n",
                                  content_type="text/csv")
        response = self.post_multipart_response(
            'ic_visit_file_view',
            "jadviser",
            body={
                "file": file,
                "visit_type": "IC Drop-In Tutoring",
                "tutoring_option": "Option 1",
                "date": "2022-09-19",
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'Invalid file')

    def test_IC_visit_file_upload_missing_required_fields(self):
        csv_content = "student_number,course_name,duration_minutes\n"
        csv_content += "1033334,CHEM 198,60\n"
        file = SimpleUploadedFile("visits.csv",
                                  csv_content.encode('utf-8'),
                                  content_type="text/csv")
        response = self.post_multipart_response(
            'ic_visit_file_view',
            "jadviser",
            body={
                "file": file,
                "visit_type": "IC Drop-In Tutoring",
                "date": "2022-09-19",
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,
                         'Missing visit_type, tutoring_option, or date')

    @patch('compass.views.api.visit.create_visits_from_file')
    def test_IC_visit_file_upload_create_visits_value_error(
            self, mock_create_visits_from_file):
        mock_create_visits_from_file.side_effect = ValueError(
            'Unable to create visits')

        csv_content = "student_number,course_name,duration_minutes\n"
        csv_content += "1033334,CHEM 198,60\n"
        file = SimpleUploadedFile("visits.csv",
                                  csv_content.encode('utf-8'),
                                  content_type="text/csv")
        response = self.post_multipart_response(
            'ic_visit_file_view',
            "jadviser",
            body={
                "file": file,
                "visit_type": "IC Drop-In Tutoring",
                "tutoring_option": "Option 1",
                "date": "2022-09-19",
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'Unable to create visits')

    def test_IC_visit_file_download(self):
        response = self.get_response('ic_visit_file_view', "jadviser")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="visit_export.csv"',
                      response['Content-Disposition'])
        self.assertEqual(response.data.replace('\r\n', '\n'),
                         "student_syskey,checkin_date,checkout_date,"
                         "duration_minutes,"
                         "visit_type,tutoring_option,course_code\n"
                         "888777333,2022-09-19T06:15:04+00:00,"
                         "2022-09-19T07:15:04+00:00,60,"
                         "IC Drop-In Tutoring,Option 1,CHEM 198\n"
                         "532353230,2022-09-20T06:15:04+00:00,"
                         "2022-09-20T07:15:04+00:00,60,"
                         "IC Drop-In Tutoring,Option 1,MATH 124\n")

    def test_visit_search_mixin_invalid_student_identifier(self):
        mixin = VisitSearchMixin()
        mixin.response_badrequest = MagicMock(return_value='bad request')

        with patch('compass.views.api.visit.valid_uwnetid',
                   return_value=False), \
                patch('compass.views.api.visit.valid_student_number',
                      return_value=False), \
                patch('compass.views.api.visit.get_person_by_uwnetid') \
                as mock_get_person_by_uwnetid, \
                patch('compass.views.api.visit.get_person_by_student_number') \
                as mock_get_person_by_student_number:
            response = mixin._visit_search_response('1234bad')

        self.assertEqual(response, 'bad request')
        mixin.response_badrequest.assert_called_once_with(
            'Invalid student identifier')
        mock_get_person_by_uwnetid.assert_not_called()
        mock_get_person_by_student_number.assert_not_called()

    def test_visit_search_mixin_person_not_found(self):
        mixin = VisitSearchMixin()
        mixin.response_notfound = MagicMock(return_value='not found')

        with patch('compass.views.api.visit.valid_uwnetid',
                   return_value=True), \
                patch('compass.views.api.visit.get_person_by_uwnetid',
                      side_effect=PersonNotFoundException):
            response = mixin._visit_search_response('lisa')

        self.assertEqual(response, 'not found')
        mixin.response_notfound.assert_called_once_with('Student not found')

    def test_visit_search_mixin_student_not_found(self):
        mixin = VisitSearchMixin()
        mixin.response_notfound = MagicMock(return_value='not found')
        mock_person = MagicMock(system_key='000123456')

        with patch('compass.views.api.visit.valid_uwnetid',
                   return_value=True), \
                patch('compass.views.api.visit.get_person_by_uwnetid',
                      return_value=mock_person), \
                patch('compass.views.api.visit.Student.objects.get',
                      side_effect=Student.DoesNotExist):
            response = mixin._visit_search_response('lisa')

        self.assertEqual(response, 'not found')
        mixin.response_notfound.assert_called_once_with('Student not found')

    @patch('compass.views.api.visit.VisitReadSerializer')
    @patch('compass.views.api.visit.Visit.objects.filter')
    @patch('compass.views.api.visit.current_term')
    @patch('compass.views.api.visit.Student.objects.get')
    @patch('compass.views.api.visit.get_person_by_student_number')
    @patch('compass.views.api.visit.valid_student_number')
    @patch('compass.views.api.visit.valid_uwnetid')
    def test_visit_search_mixin_success_by_student_number(
            self,
            mock_valid_uwnetid,
            mock_valid_student_number,
            mock_get_person_by_student_number,
            mock_student_get,
            mock_current_term,
            mock_visit_filter,
            mock_serializer):
        mixin = VisitSearchMixin()
        mixin.response_ok = MagicMock(return_value='ok')

        mock_valid_uwnetid.return_value = False
        mock_valid_student_number.return_value = True
        mock_person = MagicMock(system_key='000123456')
        mock_get_person_by_student_number.return_value = mock_person

        mock_student = MagicMock()
        mock_student_get.return_value = mock_student

        quarter_start = datetime(2026, 3, 25, tzinfo=UTC)
        mock_current_term.return_value = MagicMock(
            first_day_quarter=quarter_start)

        mock_ordered_visits = MagicMock(name='ordered_visits')
        mock_visit_filter.return_value.order_by.return_value = \
            mock_ordered_visits
        mock_serializer.return_value = MagicMock(data=[{'id': 1}])

        response = mixin._visit_search_response(' 1233338 ')

        self.assertEqual(response, 'ok')
        mock_valid_uwnetid.assert_called_once_with('1233338')
        mock_valid_student_number.assert_called_once_with('1233338')
        mock_get_person_by_student_number.assert_called_once_with('1233338')
        mock_student_get.assert_called_once_with(system_key='000123456')
        mock_visit_filter.assert_called_once_with(
            student=mock_student,
            checkin_date__gte=quarter_start)
        mock_visit_filter.return_value.order_by.assert_called_once_with(
            '-checkin_date')
        mock_serializer.assert_called_once_with(mock_ordered_visits, many=True)
        mixin.response_ok.assert_called_once_with([{'id': 1}])

    @patch('compass.views.api.visit.VisitReadSerializer')
    @patch('compass.views.api.visit.Visit.objects.filter')
    @patch('compass.views.api.visit.current_term')
    @patch('compass.views.api.visit.Student.objects.get')
    @patch('compass.views.api.visit.get_person_by_uwnetid')
    @patch('compass.views.api.visit.valid_student_number')
    @patch('compass.views.api.visit.valid_uwnetid')
    def test_visit_search_mixin_success_by_uwnetid(
            self,
            mock_valid_uwnetid,
            mock_valid_student_number,
            mock_get_person_by_uwnetid,
            mock_student_get,
            mock_current_term,
            mock_visit_filter,
            mock_serializer):
        mixin = VisitSearchMixin()
        mixin.response_ok = MagicMock(return_value='ok')

        mock_valid_uwnetid.return_value = True
        mock_valid_student_number.return_value = False
        mock_person = MagicMock(system_key='532353230')
        mock_get_person_by_uwnetid.return_value = mock_person

        mock_student = MagicMock()
        mock_student_get.return_value = mock_student

        quarter_start = datetime(2026, 3, 25, tzinfo=UTC)
        mock_current_term.return_value = MagicMock(
            first_day_quarter=quarter_start)

        mock_ordered_visits = MagicMock(name='ordered_visits')
        mock_visit_filter.return_value.order_by.return_value = \
            mock_ordered_visits
        mock_serializer.return_value = MagicMock(data=[{'id': 2}])

        response = mixin._visit_search_response(' Lisa ')

        self.assertEqual(response, 'ok')
        self.assertEqual(mock_valid_uwnetid.call_args_list,
                         [call('lisa')])
        mock_valid_student_number.assert_not_called()
        mock_get_person_by_uwnetid.assert_called_once_with('lisa')
        mock_student_get.assert_called_once_with(system_key='532353230')
        mock_visit_filter.assert_called_once_with(
            student=mock_student,
            checkin_date__gte=quarter_start)
        mock_visit_filter.return_value.order_by.assert_called_once_with(
            '-checkin_date')
        mock_serializer.assert_called_once_with(mock_ordered_visits, many=True)
        mixin.response_ok.assert_called_once_with([{'id': 2}])

    def test_external_visit_view(self):
        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        response = self.get_response('external_student_visit_view',
                                     kwargs={"identifier": "javerage"})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['visit_type'], "IC Drop-In Tutoring")
        self.assertEqual(response.data[0]['course_code'], "MATH 124")
        self.assertEqual(response.data[0]['tutoring_option'], "Option 1")
        self.assertEqual(response.data[0]['checkin_date'],
                         "2022-09-20T06:15:04Z")
        self.assertEqual(response.data[0]['checkout_date'],
                         "2022-09-20T07:15:04Z")
