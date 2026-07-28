# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from logging import getLogger

from userservice.user import UserService

from compass.views.api import BaseAPIView

logger = getLogger(__name__)


class SupportView(BaseAPIView):

    def post(self, request):
        if "clear_override" in request.data:
            us = UserService()
            logger.info(f"{us.get_original_user()} is ending impersonation of {us.get_override_user()}")
            us.clear_override()
        return self.response_ok("")
