# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.core.management import call_command
from compass.dao.storage import RADStorageDao
from compass.models.rad_data import RADWeek, RADImport
from compass.dao.rad_csv import import_data_from_csv
from logging import getLogger


logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Loads RAD data into Compass DB, defaults to current week"

    def add_arguments(self, parser):
        parser.add_argument('--week',
                            type=str,
                            default=None,
                            help="week to load, eg. '2021-spring-week-10'")

        parser.add_argument('--reload',
                            action='store_true',
                            help="reload existing data for week")
        parser.add_argument('--loadall',
                            action='store_true',
                            help="load all data found in bucket")

    def handle(self, *args, **options):
        if options['loadall']:
            file_status = self._load_all_data(options['reload'])
            call_command('generate_alert_status')
            errors = [i for i in file_status if i is not None]
            return "\n".join(errors)
        else:
            if options['week']:
                year, quarter, _, week_id = options['week'].split('-')
                if not all([year, quarter, week_id]):
                    raise ValueError(f"Invalid week: {options['week']}")
            else:
                try:
                    # Has a previous import in DB, getting following week
                    year, quarter, week_id = RADImport.get_next_import_week()
                except RADImport.DoesNotExist:
                    # No previous import in DB, get most recent week in bucket
                    latest_file = RADStorageDao().get_latest_file()
                    year, quarter, week_id = (
                        RADStorageDao.get_year_quarter_week_from_filename(
                            latest_file)
                    )
            response = self._load_week_by_year_quarter_week(year,
                                                            quarter,
                                                            week_id,
                                                            options['reload'])
            if response is not None:
                return response

            # Prebuild alert status for users
            call_command('generate_alert_status')

    def _load_week_by_year_quarter_week(self, year, quarter, week_id, reload):
        logger.info(f"Loading RAD data for {year}-{quarter}-week-{week_id}")
        rad_week = RADWeek.get_or_create_week(year=year,
                                              quarter=quarter,
                                              week=week_id)
        try:
            rad_import = RADImport.create_job(rad_week,
                                              reload=reload)
        except ValueError:
            logger.info(f"Import already exists for "
                        f"{year}-{quarter}-week-{week_id}")
            return f'Import already exists for {year}-{quarter}-week-{week_id}'
        try:
            rad_file = RADStorageDao().download_from_bucket(
                rad_import.get_filename())
            logger.info(f"Downloaded file {rad_import.get_filename()}")
            try:
                pred_file = (RADStorageDao().
                             get_pred_file_by_y_q_w(rad_week.year,
                                                    rad_week.quarter,
                                                    rad_week.week))
                logger.info(f"Downloaded prediction file")
            except FileNotFoundError:
                pred_file = None
            import_data_from_csv(rad_week, rad_file, pred_file, reload)
        except Exception as ex:
            logger.exception(ex)
            rad_import.import_status = RADImport.FAILURE
            rad_import.save()
            return (f"Failed to import RAD data for"
                    f" {year}-{quarter}-week-{week_id}")

        rad_import.import_status = RADImport.SUCCESS
        rad_import.save()
        logger.info(f"successfully imported RAD data for "
                    f"{year}-{quarter}-week-{week_id}")

    def _load_all_data(self, reload):
        files = RADStorageDao().get_files_list()
        status = []
        for file in files:
            year, quarter, week_id = (
                RADStorageDao().get_year_quarter_week_from_filename(file))

            status.append(self._load_week_by_year_quarter_week(year,
                                                               quarter,
                                                               week_id,
                                                               reload))
        return status
