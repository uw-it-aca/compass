# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json

from django.contrib.auth.models import User
from django.test import Client
from django.test.utils import override_settings
from rest_framework.authtoken.models import Token

from compass.dao.storage import RADStorageDao
from compass.models import AccessGroup
from compass.tests import ApiTest


class AnalyticsAPITest(ApiTest):
    API_TOKEN = None
    WRONG_API_TOKEN = None

    def setUp(self):
        super().setUp()
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

        token_str = f"Token {self.API_TOKEN}"
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
        wrong_token_str = f"Token {self.WRONG_API_TOKEN}"
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
    def test_upload_reduced_format(self):
        sample_json = [
            {"uw_netid": "netid123", "course_code": "MATH 101 A",
             "pred": "False"},
            {"uw_netid": "netid456", "course_code": "CHEM 142 B",
             "pred": "True"},
        ]
        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        response = self.post_response('prediction_analytics_view',
                                      body=json.dumps(sample_json))
        self.assertEqual(response.status_code, 201)
        _, latest_file = RADStorageDao().get_latest_pred_file()
        self.assertEqual(latest_file.splitlines(), [
            "uw_netid,course_code,pred",
            "netid123,MATH 101 A,False",
            "netid456,CHEM 142 B,True",
        ])

    def test_invalid_prediction_payload(self):
        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        for payload in ([], [None], {"body": "invalid"},
                        [{"uw_netid": "netid123", "pred": "False"}]):
            with self.subTest(payload=payload):
                response = self.post_response('prediction_analytics_view',
                                              body=json.dumps(payload))
                self.assertEqual(response.status_code, 400)

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

        token_str = f"Token {self.API_TOKEN}"
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)
        _, latest_file = rad_storage.get_latest_pred_file()
        self.assertIsNone(latest_file)
        response = self.post_response('prediction_analytics_view',
                                      body=test_request)
        self.assertEqual(response.status_code, 201)
        _filename, latest_file = rad_storage.get_latest_pred_file()
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
