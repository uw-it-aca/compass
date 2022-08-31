# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from memcached_clients import RestclientPymemcacheClient
import re


class CompassRestclientCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if 'pws' == service and re.match(r'^/idcard/v\d/photo', url):
            return getattr(settings, 'IDCARD_PHOTO_EXPIRES', 60 * 60 * 4)

        return 60 * 60 * 2
