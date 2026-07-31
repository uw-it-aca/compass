# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required

from supporttools.views import SpaToolView


@method_decorator(group_required(settings.COMPASS_SUPPORT_GROUP),
                  name='dispatch')
class CompassSpaToolView(SpaToolView):
    """SPA tool base for compass support tools.

    Adds COMPASS_SUPPORT_GROUP authentication to SpaToolView.
    """
    pass
