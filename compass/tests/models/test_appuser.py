# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from compass.models import AppUser


class AppUserTest(TestCase):
    def test_upsert_create(self):
        user = AppUser.objects.upsert_appuser("javerage")
        self.assertEqual(user.uwnetid, "javerage")
        self.assertEqual(len(AppUser.objects.filter(uwnetid="javerage")), 1)

    def test_upsert_update(self):
        AppUser(uwnetid="jadviser1").save()
        user = AppUser.objects.upsert_appuser("jadviser")
        self.assertEqual(user.uwnetid, "jadviser")
        self.assertEqual(len(AppUser.objects.filter(uwnetid="jadviser")), 1)
        self.assertRaises(AppUser.DoesNotExist,
                          AppUser.objects.get,
                          uwnetid="jadviser1")
