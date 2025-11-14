# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.management import call_command
from django.db.models import Count, OuterRef, Subquery
from django.conf import settings
from uw_saml.decorators import group_required
from compass.models.rad_data import RADImport, StudentAlertStatus, RADWeek
from compass.views.support import CompassSupportAPI
from compass.dao.storage import RADStorageDao


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
        current_week = RADWeek.get_most_recent_week()
        alert_data = {
            "current_week": current_week
        }
        try:
            alert_data.update({
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
            })
        except IndexError:
            pass

        try:
            file_data = []
            storage = RADStorageDao()
            file_list = storage.get_files_list()
            for file in file_list:
                year, quarter, week = (
                    storage.get_year_quarter_week_from_filename(file))
                week_string = f"{year}-{quarter}-week-{week}"
                week_key = RADWeek.build_week_key(year, quarter, week)

                import_id = "Not Imported"
                try:
                    week = RADWeek.objects.get(key=week_key)
                    data_import = imports.get(week=week)
                    import_id = data_import.id
                except ObjectDoesNotExist:
                    pass

                file_data.append({'filename': file,
                                  'week_string': week_string,
                                  'week_key': week_key,
                                  'import_id': import_id})
        except Exception:
            file_data = None

        context['file_data'] = file_data
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

        week_string = (f"{rad_import.week.year}-{rad_import.week.quarter}"
                       f"-week-{rad_import.week.week}")
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


class RetentionLoadFromFile(CompassSupportAPI):
    def put(self, request, week_string):
        call_command("load_rad_data",
                     "--week="+week_string,
                     "--reload")
        return self.response_ok({'message': f'Retention data'
                                            f' reloaded for {week_string}'})
