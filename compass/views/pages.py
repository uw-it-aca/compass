# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views.generic import TemplateView
from uw_saml.utils import get_user

class LandingView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        user = self.request.user
        print(context)
        print(user)
        print(get_user(self.request))
        return context
