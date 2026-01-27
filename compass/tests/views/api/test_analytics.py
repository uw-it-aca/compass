# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import Client
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from compass.views.api.analytics import PredictionAnalytics
from compass.tests import ApiTest
from compass.models import AccessGroup, Contact, AppUser
from django.core.management import call_command
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
