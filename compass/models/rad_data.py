# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class RADImport(models.Model):
    """
    Model to track files that have been processed by the RAD system
    """
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    JOB_STATUS_CHOICES = (
        (STARTED, 'Started'),
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure')
    )
    created_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(auto_now=True)
    week = models.OneToOneField('RADWeek',
                                on_delete=models.CASCADE)
    import_status = models.CharField(max_length=255,
                                     choices=JOB_STATUS_CHOICES)

    def get_filename(self):
        """
        Returns the filename for the import's week.
        """
        return (f"{self.week.year}-{self.week.quarter}-week-{self.week.week}"
                f"-compass-data.csv")

    @classmethod
    def get_next_import_week(cls):
        """
        Get the next week to process, assumes 10 weeks per quarter
        """

        last_week_imported = cls.objects.order_by('-week__key').first()
        if last_week_imported is None:
            raise ObjectDoesNotExist("No previous imports found")
        next_year = last_week_imported.week.year
        next_quarter = last_week_imported.week.quarter
        if last_week_imported.week.week == 10:
            if last_week_imported.week.quarter == 'autumn':
                next_year += 1
                next_quarter = 'winter'
            else:
                next_quarter = last_week_imported.week.get_next_quarter()

        next_week = (last_week_imported.week.week + 1) % 10\
            if last_week_imported.week.week != 9 else 10
        return next_year, next_quarter, next_week

    @staticmethod
    def create_job(year, quarter, week, reload=False):
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


class RADDataPoint(models.Model):
    """
    Model to store RAD scores per student, week, course
    """
    uwnetid = models.CharField(max_length=50)
    week = models.ForeignKey('RADWeek', on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    activity_score = models.FloatField()
    assignment_score = models.FloatField()
    grade_score = models.FloatField()
    prediction_score = models.FloatField()
    signin_score = models.FloatField()


class RADWeek(models.Model):
    AUT = 'AUT'
    WIN = 'WIN'
    SPR = 'SPR'
    SUM = 'SUM'
    QTR_CHOICES = (
        (AUT, 'autumn'),
        (WIN, 'winter'),
        (SPR, 'spring'),
        (SUM, 'summer')
    )
    year = models.IntegerField()
    quarter = models.CharField(max_length=255, choices=QTR_CHOICES)
    week = models.IntegerField()
    key = models.IntegerField(unique=True)

    @classmethod
    def get_or_create_week(cls, year, quarter, week):
        """
        Create week sorting key in format YYYYQWW
        """
        try:
            return cls.objects.get(year=year, quarter=quarter, week=week)
        except cls.DoesNotExist:
            qtr_map = {
                'winter': "1",
                'spring': "2",
                'summer': "3",
                'autumn': "4"
            }
            padded_week = str(week).zfill(2)
            key = int(str(year) + qtr_map[quarter] + padded_week)
            return cls.objects.create(year=year,
                                      quarter=quarter,
                                      week=week,
                                      key=key)

    def get_next_quarter(self):
        qtrs = ['winter', 'spring', 'summer', 'autumn']
        return qtrs[(qtrs.index(self.quarter) + 1) % len(qtrs)]
