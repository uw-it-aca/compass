# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.preferences import get_user_preferences
from compass.models import AppUser, UserPreference


class TestPreferences(TestCase):
    app_user = None

    def setUp(self):
        self.app_user = AppUser.objects.create(uwnetid="javerage")
        UserPreference.objects.create(
            app_user=self.app_user,
            component="caseload_filters",
            key="class",
            value="senior"
        )
        UserPreference.objects.create(
            app_user=self.app_user,
            component="caseload_filters",
            key="major",
            value="math"
        )
        UserPreference.objects.create(
            app_user=self.app_user,
            component="other_filters",
            key="admit_term",
            value="2020,autumn"
        )

    def test_get_user_preferences(self):
        prefs = get_user_preferences(self.app_user.uwnetid)
        self.assertEqual(len(prefs), 2)
        self.assertEqual(prefs["caseload_filters"]["class"], "senior")
        self.assertEqual(prefs["caseload_filters"]["major"], "math")
        self.assertEqual(prefs["other_filters"]["admit_term"], "2020,autumn")

    def test_get_user_preferences_no_user(self):
        prefs = get_user_preferences("javerage2")
        self.assertIsNone(prefs)

    def test_get_user_preferences_no_prefs(self):
        app_user = AppUser.objects.create(uwnetid="javerage2")
        prefs = get_user_preferences(app_user.uwnetid)
        self.assertEqual(len(prefs), 0)
