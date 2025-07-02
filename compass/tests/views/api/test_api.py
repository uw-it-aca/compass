# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from django.test import Client
from django.core.exceptions import PermissionDenied
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from compass.views.api import BaseAPIView
from compass.views.api.visit import VisitOMADView
from compass.tests import ApiTest
from compass.models import AccessGroup, VisitType
from compass.exceptions import OverrideNotPermitted
from rest_framework.authtoken.models import Token
from rest_framework import status


class BaseAPIViewTest(ApiTest):
    ag = None
    request = None
    view = None

    def setUp(self):
        self.ag = AccessGroup(name="Test Group",
                              access_group_id="u_astra_group1")
        self.ag.save()
        self.request = RequestFactory().get('/api/')
        self.view = BaseAPIView()

    def test_response_ok(self):
        response = self.view.response_ok("OK")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "OK")

        response = self.view.response_ok({"data": []})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"data": []})

    def test_response_created(self):
        response = self.view.response_created("OK")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "OK")

        response = self.view.response_created({"data": []})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"data": []})

    def test_response_accepted(self):
        response = self.view.response_accepted("OK")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, "OK")

        response = self.view.response_accepted({"data": []})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, {"data": []})

    def test_response_badrequest(self):
        response = self.view.response_badrequest()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Missing parameters")

        response = self.view.response_badrequest({"data": []})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"data": []})

    def test_response_unauthorized(self):
        response = self.view.response_unauthorized()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Not authorized")

        # Handle a passed exception
        try:
            raise OverrideNotPermitted()
        except OverrideNotPermitted as ex:
            response = self.view.response_unauthorized(ex)
            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data,
                             "Action not permitted while using admin override")

    def test_response_notfound(self):
        response = self.view.response_notfound()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Not found")

        response = self.view.response_notfound({"data": []})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"data": []})

    @patch('compass.models.is_group_member', return_value=True)
    @patch.object(BaseAPIView, 'valid_user_override')
    def test_access_group(self, mock_is_member, mock_is_override):
        mock_is_override.return_value = True
        ag = self.view.get_access_group(self.request, require_manager=False)
        self.assertEqual(ag.name, "Test Group")

        test_ag = AccessGroup(name="Another Group",
                              access_group_id="u_astra_group2")

        self.assertRaises(PermissionDenied, self.view.valid_access_group,
                          self.request,
                          [test_ag], require_manager=False)

        try:
            self.view.valid_access_group(self.request,
                                         [self.ag],
                                         require_manager=False)
        except PermissionDenied:
            self.fail("Access group is valid")

    def _raise_override_not_permitted(self):
        raise OverrideNotPermitted()

    @patch('compass.models.is_group_member', return_value=True)
    def test_valid_user_permission(self,
                                   mock_is_member):

        # Test Override
        with patch.object(BaseAPIView,
                          'valid_user_override',
                          side_effect=self._raise_override_not_permitted):
            self.assertRaises(PermissionDenied,
                              self.view.valid_user_permission,
                              self.request,
                              allow_override=False)
        with patch.object(BaseAPIView,
                          'valid_user_override'):
            try:
                self.view.valid_user_permission(self.request,
                                                allow_override=False)
            except PermissionDenied:
                self.fail("Override is valid")

        # Test Access Groups
        test_ags = [AccessGroup(name="Another Group",
                                access_group_id="u_astra_group2")]
        with self.assertRaises(PermissionDenied):
            self.view.get_access_group(self.request, require_manager=False)
            self.view.valid_user_permission(self.request,
                                            access_groups=test_ags,
                                            allow_override=False)
