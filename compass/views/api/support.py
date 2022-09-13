
# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from compass.views.api import BaseAPIView
from userservice.user import clear_override, get_override_user, \
    get_original_user
from rest_framework.response import Response
from rest_framework import status


class SupportView(BaseAPIView):

    def post(self, request):
        if "clear_override" in request.data:
            logging.info("{} is ending impersonation of {}".format(
                         get_original_user(request),
                         get_override_user(request)))
            clear_override(request)
        return Response("", status=status.HTTP_200_OK)
