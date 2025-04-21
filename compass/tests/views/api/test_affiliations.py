# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import ApiTest
from compass.models import Affiliation
from mock import patch


class AffiliationAPITest(ApiTest):
    @patch('compass.dao.group.is_member_of_group')
    def test_get(self, mock_is_member):
        mock_is_member.return_value = True
        response = self.get_response("access_group_affiliations", "jadviser")
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data, [])

        mock_is_member.return_value = False
        response = self.get_response("access_group_affiliations", "javerage")
        self.assertEqual(response.status_code, 401, "Unauthorized")
