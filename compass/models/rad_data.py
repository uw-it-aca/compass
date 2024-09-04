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
    def create_job(rad_week, reload=False):
        rad_import, created = (RADImport.objects.get_or_create(week=rad_week))
        if not created and not reload:
            raise ValueError(f"RAD data already imported for"
                             f" {rad_week}")
        else:
            rad_import.import_status = RADImport.STARTED
            rad_import.save()
        return rad_import


class CourseAnalyticsScores(models.Model):
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

    class Meta:
        unique_together = ('uwnetid', 'week', 'course')

    def json_data(self):
        return {'activity_score': self.activity_score,
                'assignment_score': self.assignment_score,
                'grade_score': self.grade_score,
                'prediction_score': self.prediction_score,
                'week_id': self.week.week,}

    @classmethod
    def get_rad_data_for_course(cls, year, quarter, netid, course_id):
        """
        Get course data points for a given year, quarter, course, and netid
        """
        try:
            weeks = RADWeek.objects.filter(year=year, quarter=quarter)
            return cls.objects.filter(week__in=weeks, uwnetid=netid,
                                      course=course_id).order_by("week__week")
        except RADWeek.DoesNotExist:
            return []

    @classmethod
    def get_signins_by_netid(cls, netid):
        """
        Return the last 3 quarters worth of sign in data for a student
        """

        # TODO limit this to one point per week
        try:
            current_week = RADWeek.get_most_recent_week()
            prev_term = RADWeek.get_previous_term(
                {"year": current_week.year,
                 "quarter": current_week.quarter})
            prev_prev_term = RADWeek.get_previous_term(prev_term)

            terms = [
                (current_week.year, current_week.quarter),
                (prev_term['year'], prev_term['quarter']),
                (prev_prev_term['year'], prev_prev_term['year'])
            ]

            signins_by_term = []
            for term in terms:
                term_data = cls.get_rad_data_for_course(
                    term[0], term[1], netid)
                if term_data:
                    signins_by_term.append({'year': term[0],
                                            'quarter': term[1],
                                            'data': [
                                                {week.week.week:
                                                 week.signin_score}
                                                for week in term_data]})
            return signins_by_term
        except RADWeek.DoesNotExist:
            return []

class StudentSigninAnalytics(models.Model):
    """
    Model to store weekly IdP signin data per student
    """
    uwnetid = models.CharField(max_length=50)
    week = models.ForeignKey('RADWeek', on_delete=models.CASCADE)
    signin_score = models.FloatField()

    class Meta:
        unique_together = ('uwnetid', 'week')

    @classmethod
    def get_signin_data_for_student(cls, uwnetid):
        """
        Get signin data for a given student
        """
        signins =  cls.objects.filter(uwnetid=uwnetid)
        json_data = {}
        for signin in signins:
            year_data = json_data.setdefault(signin.week.year, {})
            quarter_data = year_data.setdefault(signin.week.quarter, {})
            quarter_data[signin.week.week] = signin.signin_score

        return json_data


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

    @staticmethod
    def get_most_recent_week():
        return RADWeek.objects.order_by('-key').first()

    @staticmethod
    def get_previous_term(term):
        quarters = ['winter', 'spring', 'summer', 'autumn']
        index = quarters.index(term['quarter'])
        return {'year': term['year'] - 1, 'quarter': 'autumn'} if (
            term['quarter'] == 'winter') \
            else {'year': term['year'], 'quarter': quarters[index - 1]}
