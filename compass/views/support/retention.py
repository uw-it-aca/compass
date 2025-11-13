# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.management import call_command
from django.db.models import Count, OuterRef, Subquery
from django.conf import settings
from uw_saml.decorators import group_required
from compass.models.rad_data import RADImport, StudentAlertStatus
from compass.views.support import CompassSupportAPI


@method_decorator(group_required(settings.COMPASS_SUPPORT_GROUP),
                  name='dispatch')
class RetentionAdminView(TemplateView):
    template_name = 'retention_data_admin.html'

    def get_context_data(self, **kwargs):
        context = super(RetentionAdminView, self).get_context_data(**kwargs)
        imports = RADImport.objects.all().order_by('-week__key').annotate(
            total_scores=Count('week__courseanalyticsscores'),
            student_count=Subquery(
                RADImport.objects.filter(pk=OuterRef('pk'))
                .annotate(cnt=Count('week__courseanalyticsscores__uwnetid',
                                    distinct=True))
                .values('cnt')[:1]
            ),
            signin_scores=Subquery(
                RADImport.objects.filter(pk=OuterRef('pk'))
                .annotate(cnt=Count('week__studentsigninanalytics'))
                .values('cnt')[:1]
            )
        )
        try:
            alert_data = {
                'source_week': StudentAlertStatus.objects.all()[0].source_week,
                'total_alerts': StudentAlertStatus.objects.exclude(
                    alert_status__isnull=True).count(),
                'total_success': StudentAlertStatus.objects.filter(
                    alert_status=StudentAlertStatus.AlertStatus.SUCCESS)
                .count(),
                'total_warning': StudentAlertStatus.objects.filter(
                    alert_status=StudentAlertStatus.AlertStatus.WARNING)
                .count(),
                'total_danger': StudentAlertStatus.objects.filter(
                    alert_status=StudentAlertStatus.AlertStatus.DANGER)
                .count(),
            }
        except IndexError:
            alert_data = None
        context['imports'] = imports
        context['alert_data'] = alert_data
        return context


class RetentionManageView(CompassSupportAPI):
    def put(self, request, import_id):
        try:
            rad_import = RADImport.objects.get(id=import_id)
        except RADImport.DoesNotExist:
            return self.response_notfound(f'RAD Import id not'
                                          f' found: {import_id}')

        week_string = (f"{rad_import.week.year}-{rad_import.week.quarter}-week-"
                       f"{rad_import.week.week}")
        call_command("load_rad_data",
                     "--week=" + week_string,
                     "--reload")
        return self.response_ok({'message': f'Retention data reloaded for'
                                            f' import id: {import_id}'})

    def delete(self, request, import_id):
        try:
            rad_import = RADImport.objects.get(id=import_id)
        except RADImport.DoesNotExist:
            return self.response_notfound(f'RAD Import id not'
                                          f' found: {import_id}')

        rad_import.week.delete()
        return self.response_ok({'message': f'Retention data deleted for'
                                            f' import id: {import_id}'})


class RetentionReloadAlertsView(CompassSupportAPI):
    def put(self, request):
        call_command('generate_alert_status')
        return self.response_ok({'message': 'Student alert statuses reloaded'})
