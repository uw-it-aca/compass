# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from uw_saml.decorators import group_required
from uw_saml.utils import get_user


@method_decorator(group_required(settings.COMPASS_USERS_GROUP),
                  name='dispatch')
class LandingView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uwnetid'] = get_user(self.request)
        context['ga_key'] = getattr(settings, "GA_KEY", None)
        return context
