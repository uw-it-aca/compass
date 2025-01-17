# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import CompassTestCase
from compass.models import UserPreference


class UserPreferenceTest(CompassTestCase):
    def test_validation(self):
        self.assertTrue(UserPreference.validate_preference("caseload_filters",
                                                           "class"))
        self.assertFalse(UserPreference.validate_preference("caseload_filters",
                                                            "invalid_key"))
        self.assertFalse(UserPreference.validate_preference("other_component",
                                                            "invalid_key"))
