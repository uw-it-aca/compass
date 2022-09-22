# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from memcached_clients import RestclientPymemcacheClient
import re

ONE_MINUTE = 60
ONE_HOUR = ONE_MINUTE * 60
ONE_DAY = ONE_HOUR * 24


class CompassRestclientCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if 'pws' == service:
            if re.match(r'^/idcard/v1/photo)', url):
                return ONE_DAY * 5
            return ONE_HOUR * 4
        elif 'sws' == service:
            return ONE_DAY
        elif 'gws' == service:
            return ONE_MINUTE * 15

        return ONE_HOUR
