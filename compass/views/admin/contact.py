# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from compass.models import OMADContactQueue


@method_decorator(login_required, name='dispatch')
class OMADContactAdminView(TemplateView):
    template_name = 'omad_contact_admin.html'

    def get_context_data(self, **kwargs):
        context = super(OMADContactAdminView, self).get_context_data(**kwargs)
        contacts = OMADContactQueue.objects.all()
        context['contacts'] = contacts
        return context
