# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.db.models import Count, OuterRef, Subquery

from compass.dao.storage import RADStorageDao
from compass.models.rad_data import RADImport, RADWeek, StudentAlertStatus
from compass.views.support import CompassSupportAPI


def build_retention_page_data():
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
        file_list = storage.get_analytics_file_list()
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
    try:
        prediction_files = []
        storage = RADStorageDao()
        pred_file_list = storage.get_pred_file_list()
        for file in pred_file_list:
            prediction_files.append({'filename': file})
    except Exception:
        prediction_files = None

    source_week = alert_data.get('source_week')
    cw = alert_data.get('current_week')
    return {
        'imports': [
            {
                'id': imp.id,
                'year': imp.week.year,
                'quarter': imp.week.quarter,
                'week': imp.week.week,
                'week_key': imp.week.key,
                'created_date': imp.created_date.isoformat()
                if imp.created_date else None,
                'processed_date': imp.processed_date.isoformat()
                if imp.processed_date else None,
                'import_status': imp.get_import_status_display(),
                'student_count': imp.student_count,
                'total_scores': imp.total_scores,
                'signin_scores': imp.signin_scores,
                'prediction_filename': imp.prediction_filename,
            }
            for imp in imports
        ],
        'alert_data': {
            'source_week': {
                'year': source_week.year,
                'quarter': source_week.quarter,
                'week': source_week.week,
            } if source_week else None,
            'current_week': {
                'year': cw.year,
                'quarter': cw.quarter,
                'week': cw.week,
            } if cw else None,
            'total_alerts': alert_data.get('total_alerts', 0),
            'total_success': alert_data.get('total_success', 0),
            'total_warning': alert_data.get('total_warning', 0),
            'total_danger': alert_data.get('total_danger', 0),
        },
        'file_data': file_data,
        'prediction_files': prediction_files,
    }


class RetentionPageDataView(CompassSupportAPI):
    def get(self, request):
        return self.response_ok(build_retention_page_data())


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
