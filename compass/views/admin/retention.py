# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from compass.models.rad_data import RADImport, RADWeek
from compass.views.api import BaseAPIView


@method_decorator(login_required, name='dispatch')
class RetentionAdminView(TemplateView):
    template_name = 'retention_data_admin.html'

    def get_context_data(self, **kwargs):
        context = super(RetentionAdminView, self).get_context_data(**kwargs)
        imports = RADImport.objects.all().order_by('-week__key')
        context['imports'] = imports
        return context

@method_decorator(login_required, name='dispatch')
class RetentionReloadView(BaseAPIView):
    def get(self, request, import_id):
        # try:
        #     rad_import = RADImport.objects.get(id=import_id)
        # except RADImport.DoesNotExist:
        #     return self.response_notfound(f'RAD Import id not found: {import_id}')
        #
        # rad_import.reload_retention_data()
        return self.response_ok({'message': f'Retention data reloaded for import id: {import_id}'})
