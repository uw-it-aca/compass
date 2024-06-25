# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from compass.dao.storage import RADStorageDao
from compass.models.rad_data import RADWeek, RADImport
from django.core.exceptions import ObjectDoesNotExist

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
            year, quarter, week_id = options['week'].split('-')
            if year is None or quarter is None or week_id is None:
                raise ValueError(f"Invalid week: {options['week']}")
        else:
            print("NEXT")
            year, quarter, week_id = RADImport.get_next_week()
        except ObjectDoesNotExist:
        # Get most recent in bucket
        latest_file = RADStorageDao().get_latest_file()


        year, quarter, week_id = (
            RADStorageDao.get_year_quarter_week_from_filename(
                latest_file)
        )
    rad_import = self.create_job(year,
                                 quarter,
                                 week_id,
                                 reload=options['reload'])
    rad_file = RADStorageDao().download_from_bucket(
        rad_import.get_filename())
    print(rad_file)
    # TODO: Process rad_file


def create_job(self, year, quarter, week, reload=False):
    rad_week = RADWeek.get_or_create_week(year=year,
                                          quarter=quarter,
                                          week=week)

    rad_import, created = (RADImport.objects.
                           get_or_create(week=rad_week,
                                         import_status=RADImport.STARTED))
    if not created and not reload:
        raise ValueError(f"RAD data already imported for"
                         f" {year}-{quarter}-{week}")
    return rad_import







