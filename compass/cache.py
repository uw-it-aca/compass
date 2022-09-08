# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from memcached_clients import RestclientPymemcacheClient

ONE_MINUTE = 60
ONE_HOUR = 60 * 60


class CompassRestclientCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if 'pws' == service:
            return ONE_HOUR * 4

        elif 'gws' == service:
            return ONE_MINUTE * 15

        return ONE_HOUR
