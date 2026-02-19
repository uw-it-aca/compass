# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import Client
from django.contrib.auth.models import User
from django.test.utils import override_settings
from compass.tests import ApiTest
from compass.models import AccessGroup
from compass.dao.storage import RADStorageDao
from rest_framework.authtoken.models import Token
import json


class AnalyticsAPITest(ApiTest):
    API_TOKEN = None
    WRONG_API_TOKEN = None

    def setUp(self):
        super(AnalyticsAPITest, self).setUp()
        AccessGroup(name="OMAD", access_group_id="u_astra_group1").save()
        user = User.objects.create_user(username='era-predictions-api',
                                        password='12345')
        self.API_TOKEN = Token.objects.create(user=user).key
        other_user = User.objects.create_user(username='foo',
                                              password='12345')
        self.WRONG_API_TOKEN = Token.objects.create(user=other_user).key

    @override_settings(STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.memory.InMemoryStorage',
        }
    })
    def test_api_auth(self):
        sample_json = {
            "body": [
                {
                    "": "0",
                    "system_key": "12345",
                    "student_no": "54321",
                    "uw_netid": "netid123",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                },
            ]
        }
        test_request = json.dumps(sample_json)

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        response = self.post_response('prediction_analytics_view',
                                      body=test_request)
        self.assertEqual(response.status_code, 201)
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION="BAD TOKEN")

        response = self.post_response('prediction_analytics_view',
                                      test_request)
        self.assertEqual(response.status_code, 401)
        wrong_token_str = "Token %s" % self.WRONG_API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=wrong_token_str)

        response = self.post_response('prediction_analytics_view',
                                      body=test_request)
        self.assertEqual(response.status_code, 401)

    @override_settings(STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.memory.InMemoryStorage',
        }
    })
    def test_upload(self):
        rad_storage = RADStorageDao()
        sample_json = {
            "body": [
                {
                    "": "0",
                    "system_key": "12345",
                    "student_no": "54321",
                    "uw_netid": "netid123",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                },
                {
                    "": "1",
                    "system_key": "12346",
                    "student_no": "54322",
                    "uw_netid": "netid456",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "True"
                },
                {
                    "": "2",
                    "system_key": "12347",
                    "student_no": "54323",
                    "uw_netid": "netid789",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                }
            ]
        }
        test_request = json.dumps(sample_json)

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        filename, latest_file = rad_storage.get_latest_pred_file()
        self.assertIsNone(latest_file)
        response = self.post_response('prediction_analytics_view',
                                      body=test_request)
        self.assertEqual(response.status_code, 201)
        filename, latest_file = rad_storage.get_latest_pred_file()
        self.assertIsNotNone(latest_file)
        expected_rows = [
            "uw_netid,course_code,pred",
            "netid123,MATH 101 A,False",
            "netid456,MATH 101 A,True",
            "netid789,MATH 101 A,False"
        ]
        latest_file_rows = [line.strip() for line in
                            latest_file.strip().split("\n")]
        self.assertEqual(latest_file_rows, expected_rows)
