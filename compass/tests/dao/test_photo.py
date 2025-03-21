# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.photo import PhotoDAO


class TestPhoto(TestCase):
    dao = None

    def setUp(self):
        self.dao = PhotoDAO()

    def test_avatar_url(self):
        url = self.dao.get_avatar_url("https://www.test.com", 200)
        self.assertEqual(url, "https://www.test.com")

        url = self.dao.get_avatar_url(
            "https://www.gravatar.com/avatar/123?s=100",
            200)
        self.assertEqual(url, "https://www.gravatar.com/avatar/123?s=200&d=mm")
