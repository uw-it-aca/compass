# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class LandingView(TemplateView):
    template_name = 'index.html'
