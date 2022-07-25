# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import random
import string
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from uw_pws import PWS
from urllib.parse import urlparse, urlunparse
from restclients_core.exceptions import DataFailureException, InvalidNetID


class PhotoDAO():

    def __init__(self):
        super().__init__()

    def cache_key(self, key):
        return 'idphoto-key-{}'.format(key)

    def get_photo(self, photo_key):
        data = cache.get(self.cache_key(photo_key))
        cache.delete(self.cache_key(photo_key))

        if data is None:
            raise ObjectDoesNotExist()

        return PWS().get_idcard_photo(
            data.get('reg_id'), size=data.get('image_size'))

    def get_photo_url(self, reg_id, image_size="small"):
        """ Returns a url for the IDPhoto
        """
        if PWS().valid_uwregid(reg_id):
            photo_key = ''.join(random.SystemRandom().choice(
                string.ascii_lowercase + string.digits) for _ in range(16))

            data = {'reg_id': reg_id, 'image_size': image_size}
            expires = getattr(settings, 'IDCARD_TOKEN_EXPIRES', 60 * 60)
            cache.set(self.cache_key(photo_key), data, timeout=expires)
            return reverse('photo', kwargs={'photo_key': photo_key})

    def get_avatar_url(self, url, image_size):
        """ Modifies the passed url based on image_size
        """
        url_parts = urlparse(url)
        if 'gravatar.com' in url_parts.netloc:
            new_parts = url_parts._replace(
                query='s={}&d=mm'.format(image_size))
            return urlunparse(new_parts)
        return url


class UserServiceDAO():

    @classmethod
    def is_netid(cls, username):
        pws = PWS()
        error_msg = "No override user supplied, please enter a UWNetID"
        if username is not None and len(username) > 0:
            try:
                user = pws.get_entity_by_netid(username.lower())
                if username.lower() == user.uwnetid:
                    error_msg = None
                else:
                    error_msg = "Current netid: {}, Prior netid: ".format(
                        user.uwnetid)
            except InvalidNetID:
                error_msg = "Not a valid UWNetID: "
            except DataFailureException as err:
                error_msg = "Error ({}) {}: ".format(err.status, err.msg)
        return error_msg
