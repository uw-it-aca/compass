# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import UserPreference
from compass.tests import CompassTestCase


class UserPreferenceTest(CompassTestCase):
    def test_validation(self):
        self.assertTrue(UserPreference.validate_preference("caseload_filters",
                                                           "class"))
        self.assertFalse(UserPreference.validate_preference("caseload_filters",
                                                            "invalid_key"))
        self.assertFalse(UserPreference.validate_preference("other_component",
                                                            "invalid_key"))
