# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from compass.dao.person import get_person_by_uwregid
from compass.dao.term import current_week, current_term, week_of_term
from compass.dao import current_datetime


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

        last_week_imported = (cls.objects.filter(import_status=cls.SUCCESS)
                              .order_by('-week__key').first())
        if last_week_imported is None:
            raise cls.DoesNotExist("No previous imports found")
        next_year = last_week_imported.week.year
        next_quarter = last_week_imported.week.quarter
        if last_week_imported.week.week == 10:
            if last_week_imported.week.quarter == 'autumn':
                next_year += 1
                next_quarter = 'winter'
            else:
                next_quarter = last_week_imported.week.get_next_quarter()

        next_week = 10 if last_week_imported.week.week == 9 else \
            (last_week_imported.week.week + 1) % 10
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
    prediction_score = models.FloatField(null=True)

    class Meta:
        unique_together = ('uwnetid', 'week', 'course')

    def json_data(self):
        return {'activity_score':
                convert_score_range(self.activity_score),
                'assignment_score':
                    convert_score_range(self.assignment_score),
                'grade_score':
                    convert_score_range(self.grade_score),
                'prediction_score':
                    self.prediction_score,
                'week_id':
                    self.week.week}

    def is_alert_status(self):
        return self.prediction_score is not None and self.prediction_score > 0

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
    def get_course_alert_status(cls, netid, year, quarter, week, course_id):
        try:
            scores = cls.objects.get(uwnetid=netid,
                                     week__year=year,
                                     week__quarter=quarter,
                                     week__week=week,
                                     course=course_id)
            return scores.is_alert_status()
        except cls.DoesNotExist:
            return False

    @classmethod
    def add_alert_status_to_schedules(cls, schedules, uwregid):
        """
        Add alert status to schedule
        """
        person = get_person_by_uwregid(uwregid)
        netid = person.uwnetid
        week = current_week()

        for index in schedules.keys():
            schedule = schedules[index]
            for section in schedule['sections']:
                course_id = (f"{section['curriculum_abbr']} "
                             f"{section['course_number']} "
                             f"{section['section_id']}")
                alert_status = cls.get_course_alert_status(netid,
                                                           schedule['year'],
                                                           schedule['quarter'],
                                                           week,
                                                           course_id)
                section['alert_status'] = alert_status
        return schedules

    @classmethod
    def add_alert_class_to_caseload(cls, caseload):
        """
        Add alert status to caseload
        """
        for student in caseload:
            student['analytics_alert'] = cls.get_alert_class_for_student(
                student['uwnetid'])
        return caseload

    @classmethod
    def add_alert_class_to_contacts(cls, contacts):
        alerts_by_netid = {}
        for contact in contacts:
            netid = contact['student']['uwnetid']
            if netid in alerts_by_netid:
                contact['student']['analytics_alert'] = alerts_by_netid[netid]
            else:
                alert_class = cls.get_alert_class_for_student(netid)
                alerts_by_netid[netid] = alert_class
                contact['student']['analytics_alert'] = alert_class
        return contacts

    @classmethod
    def get_alert_class_for_student(cls, uwnetid):
        term = current_term()
        week = week_of_term(term, current_datetime().date())

        # RAD data is only available after the first week
        if week > 1:
            # Show last week's RAD data
            week = week - 1
            alert_count = 0
            if week > 1:
                course_analytics = cls.objects.filter(
                    uwnetid=uwnetid,
                    week__year=term.year,
                    week__quarter=term.quarter,
                    week__week=week
                )

                for course in course_analytics:
                    if course.is_alert_status():
                        alert_count += 1
            if alert_count == 0:
                alert_class = 'success'
            elif len(course_analytics) == alert_count:
                alert_class = 'danger'
            else:
                alert_class = 'warning'
            return alert_class


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
        signins = cls.objects.filter(uwnetid=uwnetid)
        json_data = {}
        for signin in signins:
            year_data = json_data.setdefault(signin.week.year, {})
            quarter_data = year_data.setdefault(signin.week.quarter, {})
            quarter_data[signin.week.week] = convert_score_range(
                signin.signin_score)

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
    def get_quarter_number(cls, sis_term):
        qtr_map = {
            'winter': "1",
            'spring': "2",
            'summer': "3",
            'autumn': "4"
        }
        return qtr_map[sis_term]

    @classmethod
    def get_or_create_week(cls, year, quarter, week):
        """
        Create week sorting key in format YYYYQWW
        """
        try:
            return cls.objects.get(year=year, quarter=quarter, week=week)
        except cls.DoesNotExist:

            padded_week = str(week).zfill(2)
            key = int(f"{year}{cls.get_quarter_number(quarter)}{padded_week}")
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


def convert_score_range(old_value):
    old_min, old_max = -5.0, 5.0
    new_min, new_max = 0, 100
    new_value = ((old_value - old_min) / (old_max - old_min)) * (
        new_max - new_min) + new_min
    return round(new_value)
