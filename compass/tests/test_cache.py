# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase

from compass.cache import CompassRestclientCache


class TestCache(TestCase):
    cache = None

    def setUp(self):
        self.cache = CompassRestclientCache()

    def test_cache_expiration_time(self):
        photo_time = self.cache.get_cache_expiration_time('pws',
                                                          '/idcard/v1/photo')
        self.assertEqual(photo_time, 432000)

        pws_time = self.cache.get_cache_expiration_time('pws', '/person/')
        self.assertEqual(pws_time, 14400)

        sws_term_time = self.cache.get_cache_expiration_time(
            'sws', '/student/v5/term/current.json')
        self.assertEqual(sws_term_time, 86400)

        sws_registration_time = self.cache.get_cache_expiration_time(
            'sws', '/student/v5/registration.json')
        self.assertEqual(sws_registration_time, 900)

        sws_not_found_time = self.cache.get_cache_expiration_time(
            'sws', '/student/v5/registration.json', status=404)
        self.assertEqual(sws_not_found_time, 420)

        sws_unavailable_time = self.cache.get_cache_expiration_time(
            'sws', '/student/v5/registration.json', status=503)
        self.assertEqual(sws_unavailable_time, 420)

        gws_time = self.cache.get_cache_expiration_time('gws', '/group/')
        self.assertEqual(gws_time, 900)

        compass_visits_time = self.cache.get_cache_expiration_time(
            'compass_visits', '/api/v1/visitadminlist')
        self.assertIsNone(compass_visits_time)

        other_time = self.cache.get_cache_expiration_time('other', '/other/')
        self.assertEqual(other_time, 3600)
