# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao import PwsDAO
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic import View
from restclients_core.exceptions import DataFailureException


class PhotoView(View):
    cache_time = 60 * 60 * 4
    date_format = '%a, %d %b %Y %H:%M:%S GMT'

    def get(self, request, *args, **kwargs):
        photo_key = kwargs.get('photo_key')
        now = datetime.utcnow()
        expires = now + timedelta(seconds=self.cache_time)
        try:
            pws_dao = PwsDAO()
            photo = pws_dao.get_photo(photo_key)
            response = StreamingHttpResponse(photo,
                                             content_type='image/jpeg')
            response['Cache-Control'] = 'public,max-age={}'.format(
                self.cache_time)
            response['Expires'] = expires.strftime(self.date_format)
            response['Last-Modified'] = now.strftime(self.date_format)
            return response
        #except DataFailureException:
        #    return HttpResponse(status=503)
        except ObjectDoesNotExist:
            status = 304 if ('HTTP_IF_MODIFIED_SINCE' in request.META) else 404
            return HttpResponse(status=status)
