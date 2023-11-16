# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import ApiTest
from compass.models import AccessGroup, AppUser, EligibilityType
import json
from mock import patch


class AccessGroupAPITest(ApiTest):
    ag = None

    def setUp(self):
        super(AccessGroupAPITest, self).setUp()
        self.ag = AccessGroup(name="Test Group",
                              access_group_id="u_astra_group1")
        self.ag.save()

    @patch('compass.dao.group.is_member_of_group')
    def test_get_eligibility(self, mock_is_member):
        mock_is_member.return_value = True
        resp = self.get_response("access_group_view",
                                 "javerage")
        response = json.loads(resp.content)
        self.assertEqual(response[0]['name'], "Test Group")

    def test_unauthorized(self, ):
        resp = self.get_response("access_group_view",
                                 "javerage")
        self.assertEqual(resp.status_code, 401)
