# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import CompassTestCase
from compass.models.rad_data import RADWeek, RADImport


class RADDataTest(CompassTestCase):
    def test_create_week(self):
        week1 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=10)
        self.assertIsNotNone(week1)
        self.assertEqual(week1.year, 2021)
        self.assertEqual(week1.quarter, 'spring')
        self.assertEqual(week1.week, 10)
        self.assertEqual(week1.key, 2021210)
        week2 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=10)
        self.assertEqual(week2.key, 2021210)
        self.assertEqual(week2.id, week1.id)

    def test_week_padding(self):
        week1 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=1)
        self.assertEqual(week1.key, 2021201)
        week2 = RADWeek.get_or_create_week(year=2021,
                                           quarter='spring',
                                           week=10)
        self.assertEqual(week2.key, 2021210)

    def test_get_next(self):
        spr_week = RADWeek.get_or_create_week(year=2021,
                                              quarter='spring',
                                              week=10)
        aut_week = RADWeek.get_or_create_week(year=2021,
                                              quarter='autumn',
                                              week=5)

        self.assertEqual(spr_week.get_next_quarter(), 'summer')
        self.assertEqual(aut_week.get_next_quarter(), 'winter')

    def test_get_next_week(self):
        w1 = RADWeek.get_or_create_week(year=2021,
                                        quarter='spring',
                                        week=10)
        w2 = RADWeek.get_or_create_week(year=2021,
                                        quarter='autumn',
                                        week=10)
        RADImport.objects.create(week=w1,
                                 import_status=RADImport.STARTED)

        year, quarter, week = RADImport.get_next_import_week()
        self.assertEqual(year, 2021)
        self.assertEqual(quarter, 'summer')
        self.assertEqual(week, 1)
        RADImport.objects.create(week=w2,
                                 import_status=RADImport.STARTED)
        year, quarter, week = RADImport.get_next_import_week()
        self.assertEqual(year, 2022)
        self.assertEqual(quarter, 'winter')
        self.assertEqual(week, 1)

    def test_create_job(self):
        rad_import = RADImport.create_job(year=2021,
                                          quarter='spring',
                                          week=10)
        self.assertEqual(rad_import.week.year, 2021)
        with self.assertRaises(ValueError):
            RADImport.create_job(year=2021,
                                 quarter='spring',
                                 week=10)
        RADImport.create_job(year=2021,
                             quarter='spring',
                             week=10,
                             reload=True)
