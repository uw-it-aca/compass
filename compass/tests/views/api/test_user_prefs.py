# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import patch
from compass.tests import ApiTest
from compass.models import UserPreference, AppUser


class UserPrefsAPITest(ApiTest):
    APP_USER = None

    def setUp(self):
        super(UserPrefsAPITest, self).setUp()
        self.APP_USER = AppUser.objects.create(uwnetid="javerage")

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_put(self, mock_is_member):
        put_body = {
            "caseload_filters": {
                "class": "senior"
            }
        }
        r = self.put_response('user_preference_view',
                              self.APP_USER,
                              put_body)
        prefs = UserPreference.objects.all()
        self.assertEqual(len(prefs), 1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(prefs[0].component, "caseload_filters")
        self.assertEqual(prefs[0].key, "class")
        self.assertEqual(prefs[0].value, "senior")

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_invalid_key(self, mock_is_member):
        put_body = {
            "caseload_filters": {
                "class": "senior",
                "invalid_key": "value"
            }
        }
        r = self.put_response('user_preference_view',
                              self.APP_USER,
                              put_body)
        prefs = UserPreference.objects.all()
        self.assertEqual(len(prefs), 1)
        self.assertEqual(r.status_code, 202)
        self.assertIn("invalid_key", r.content.decode())

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_remove_preference(self, mock_is_member):
        UserPreference.objects.create(
            app_user=self.APP_USER,
            component="caseload_filters",
            key="class",
            value="senior"
        )
        prefs = UserPreference.objects.all()
        self.assertEqual(len(prefs), 1)

        put_body = {
            "caseload_filters": {}
        }
        r = self.put_response('user_preference_view',
                              self.APP_USER,
                              put_body)
        prefs = UserPreference.objects.all()
        self.assertEqual(len(prefs), 0)
        self.assertEqual(r.status_code, 200)
