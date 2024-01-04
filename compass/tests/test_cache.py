# Copyright 2024 UW-IT, University of Washington
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

        sws_time = self.cache.get_cache_expiration_time('sws', '/student/')
        self.assertEqual(sws_time, 86400)

        gws_time = self.cache.get_cache_expiration_time('gws', '/group/')
        self.assertEqual(gws_time, 900)

        other_time = self.cache.get_cache_expiration_time('other', '/other/')
        self.assertEqual(other_time, 3600)
