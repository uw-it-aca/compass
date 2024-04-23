# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import random
import string
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from uw_pws import PWS
from urllib.parse import urlparse, urlunparse


class PhotoDAO():
    def cache_key(self, key):
        return 'idphoto-key-{}'.format(key)

    def generate_photo_key(self, image_size='medium'):
        photo_key = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(16))

        data = {'image_size': image_size}
        expires = getattr(settings, 'IDCARD_TOKEN_EXPIRES', 60 * 5)
        cache.set(self.cache_key(photo_key), data, timeout=expires)
        return photo_key

    def get_photo(self, uwregid, photo_key):
        data = cache.get(self.cache_key(photo_key))

        if data is None:
            raise ObjectDoesNotExist()

        return PWS().get_idcard_photo(uwregid, size=data.get('image_size'))

    def get_avatar_url(self, url, image_size):
        """ Modifies the passed url based on image_size
        """
        url_parts = urlparse(url)
        if 'gravatar.com' in url_parts.netloc:
            new_parts = url_parts._replace(
                query='s={}&d=mm'.format(image_size))
            return urlunparse(new_parts)
        return url
