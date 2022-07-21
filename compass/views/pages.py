# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from django.conf import settings
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import TemplateView
from uw_saml.utils import get_user


class LandingView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        verify_access()
        context = super().get_context_data(**kwargs)
        context['user_netid'] = get_user(self.request)
        context['user_role'] = "manager"
        context['signout_url'] = reverse('saml_logout')
        context['ga_key'] = getattr(settings, "GOOGLE_ANALYTICS_KEY", None)
        return context
