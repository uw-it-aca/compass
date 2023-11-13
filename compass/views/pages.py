# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from compass.views.decorators import person_required


@method_decorator(person_required, name='dispatch')
class LandingView(TemplateView):
    template_name = 'index.html'
