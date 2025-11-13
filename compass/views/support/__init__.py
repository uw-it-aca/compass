# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.utils.decorators import method_decorator
from django.conf import settings
from uw_saml.decorators import group_required
from compass.views.api import BaseAPIView


@method_decorator(group_required(settings.COMPASS_SUPPORT_GROUP),
                  name='dispatch')
class CompassSupportAPI(BaseAPIView):
    pass
