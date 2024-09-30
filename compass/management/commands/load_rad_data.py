# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from compass.dao.storage import RADStorageDao
from compass.models.rad_data import RADWeek, RADImport, CourseAnalyticsScores
from django.core.exceptions import ObjectDoesNotExist
from compass.dao.rad_csv import import_data_from_csv
from compass.dao.person import get_person_by_uwnetid
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
            return self._load_week_by_year_quarter_week(year,
                                                        quarter,
                                                        week_id,
                                                        options['reload'])

    def _load_week_by_year_quarter_week(self, year, quarter, week_id, reload):
        rad_week = RADWeek.get_or_create_week(year=year,
                                              quarter=quarter,
                                              week=week_id)
        try:
            rad_import = RADImport.create_job(rad_week,
                                              reload=reload)
        except ValueError:
            return f'Import already exists for {year}-{quarter}-week-{week_id}'
        try:
            rad_file = RADStorageDao().download_from_bucket(
                rad_import.get_filename())
            import_data_from_csv(rad_week, rad_file, reload)
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
