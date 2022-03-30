# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = "index.html"
