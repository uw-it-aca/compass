# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import ApiTest
from compass.models import Affiliation


class AffiliationAPITest(ApiTest):
    def test_get(self):
        response = self.get_response("access_group_affiliations", "jadviser")
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.data, [])

        response = self.get_response("access_group_affiliations", "javerage")
        self.assertEqual(response.status_code, 401, "Unauthorized")
        self.assertEqual(response.data, [])
