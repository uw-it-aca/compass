# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from compass.dao.storage import RADStorageDao
from compass.models.rad_data import RADWeek, RADImport, RADDataPoint
from django.core.exceptions import ObjectDoesNotExist
from compass.dao.rad_csv import import_data_from_csv
from compass.dao.person import get_person_by_uwnetid


class Command(BaseCommand):
    help = "Loads RAD data into Compass DB, defaults to current week"

    def add_arguments(self, parser):
        parser.add_argument('--week',
                            type=str,
                            default=None,
                            help="week to load, eg. '2021-spring-week-10'")

        parser.add_argument('--reload',
                            type=bool,
                            default=False,
                            help="reload existing data for week")

    def handle(self, *args, **options):
        if options['week']:
            year, quarter, _, week_id = options['week'].split('-')
            if not year or not quarter or not week_id:
                raise ValueError(f"Invalid week: {options['week']}")
        else:
            try:
                year, quarter, week_id = RADImport.get_next_import_week()
            except ObjectDoesNotExist:
                # Get most recent in bucket
                latest_file = RADStorageDao().get_latest_file()

                year, quarter, week_id = (
                    RADStorageDao.get_year_quarter_week_from_filename(
                        latest_file)
                )
        rad_import = RADImport.create_job(year,
                                          quarter,
                                          week_id,
                                          reload=options['reload'])
        try:
            rad_file = RADStorageDao().download_from_bucket(
                rad_import.get_filename())
            import_data_from_csv(rad_file, rad_import)
        except Exception as ex:
            rad_import.import_status = RADImport.FAILURE
            rad_import.save()

        rad_import.import_status = RADImport.SUCCESS
        rad_import.save()
