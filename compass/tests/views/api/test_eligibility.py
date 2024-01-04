# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import ApiTest
from compass.models import AccessGroup, AppUser, EligibilityType
import json
from mock import patch


class EligibilityAPITest(ApiTest):
    ag = None
    et = None

    def setUp(self):
        super(EligibilityAPITest, self).setUp()
        self.ag = AccessGroup(name="Test Group",
                              access_group_id="u_astra_group1")
        self.ag.save()
        self.et = EligibilityType(access_group=self.ag,
                                  name="eligibility",
                                  slug="eligibility")
        self.et.save()
        self.et2 = EligibilityType(access_group=self.ag,
                                   name="eligibility2",
                                   slug="eligibility2")
        self.et2.save()

    @patch('compass.dao.group.is_member_of_group')
    def test_get_eligibility(self, mock_is_member):
        mock_is_member.return_value = True
        resp = self.get_response("eligibility_view",
                                 "javerage")
        response = json.loads(resp.content)
        self.assertEqual(len(response), 2)

    def test_unauthorized(self, ):
        resp = self.get_response("eligibility_view",
                                 "javerage")
        self.assertEqual(resp.status_code, 401)
