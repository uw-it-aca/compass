# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import logging
from compass.views.api import BaseAPIView
from userservice.user import UserService


class SupportView(BaseAPIView):

    def post(self, request):
        if "clear_override" in request.data:
            us = UserService()
            logging.info("{} is ending impersonation of {}".format(
                         us.get_original_user(), us.get_override_user()))
            us.clear_override()
        return self.response_ok("")
