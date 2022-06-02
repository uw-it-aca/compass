# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from uw_saml.utils import get_user


class PageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['netid'] = get_user(self.request)
        context['ga_key'] = getattr(settings, "GOOGLE_ANALYTICS_KEY", None)
        return context


@method_decorator(verify_access(), name='dispatch')
class LandingView(PageView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        return context
