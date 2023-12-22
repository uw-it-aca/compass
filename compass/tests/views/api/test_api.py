# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from django.test import Client
from django.core.exceptions import PermissionDenied
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from compass.views.api.visit import VisitOMADView
from compass.tests import ApiTest
from compass.models import AccessGroup, VisitType
from rest_framework.authtoken.models import Token
from compass.views.api import BaseAPIView
from compass.exceptions import OverrideNotPermitted


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
