# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import Client
from django.contrib.auth.models import User
from django.test.utils import override_settings
from compass.tests import ApiTest
from compass.models import AccessGroup
from compass.dao.storage import RADStorageDao
from rest_framework.authtoken.models import Token


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

    def test_api_auth(self):
        test_request = """
        ,system_key,student_no,uw_netid,yrq,course_code,pred
        0,0000001,8123456,javerage  ,20252,TRAIN 100 A,False
        """
        test_request = "\n".join([line.strip() for line in test_request.strip()
                                 .split("\n")])

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
        test_request = """
        ,system_key,student_no,uw_netid,yrq,course_code,pred
        0,0000001,8123456,javerage  ,20252,TRAIN 100 A,False
        1,0000002,1000002,jsmith    ,20252,BIOL 101 A,True
        2,0000003,8654321,lisa      ,20252,TRAIN 100 A,False
        """
        test_request = "\n".join([line.strip() for line in test_request.strip()
                                 .split("\n")])

        token_str = "Token %s" % self.API_TOKEN
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_AUTHORIZATION=token_str)

        self.assertIsNone(rad_storage.get_latest_pred_file())
        response = self.post_response('prediction_analytics_view',
                                      body=test_request)
        self.assertEqual(response.status_code, 201)
        latest_file = rad_storage.get_latest_pred_file()
        self.assertIsNotNone(latest_file)
        self.assertEqual(latest_file.strip(), test_request.strip())
