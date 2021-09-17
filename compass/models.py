# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass import utilities
from datetime import datetime, date
from django.db import models
from django.utils import timezone
from uw_sws.term import get_current_term, get_term_by_year_and_quarter
from uw_sws import SWS_TIMEZONE


class TermManager(models.Manager):

    def get_current_term(self):
        curr_date = timezone.now()
        return self.get_term_for_date(curr_date)

    def get_term_for_date(self, date):
        """
        Return term intersecting with supplied date

        :param date: date to return term for
        :type date: datetime.datetime
        """
        term = (Term.objects
                .filter(first_day_quarter__lte=date)
                .filter(grade_submission_deadline__gte=date)).first()
        return term

    def get_or_create_term_from_sis_term_id(self, sis_term_id=None):
        """
        Creates and/or queries for Term matching sis_term_id. If sis_term_id
        is not defined, creates and/or queries for Term object for current
        sws term.

        :param sis_term_id: sis term id to return Term object for
        :type sis_term_id: str
        """
        if sis_term_id is None:
            # try to lookup the current term based on the date
            term = self.get_current_term()
            if term:
                # return current term
                return term, False

        if sis_term_id:
            # lookup sws term object for supplied sis term id
            year, quarter = sis_term_id.split("-")
            sws_term = get_term_by_year_and_quarter(int(year), quarter)
        else:
            # lookup sws term object for current term
            sws_term = get_current_term()
        return self.get_or_create_from_sws_term(sws_term)

    def get_or_create_from_sws_term(self, sws_term):
        """
        Creates and/or queries for Term for sws_term object. If Term for
        sws_term is not defined in the database, a Term object is created.

        :param sws_term: sws_term object to create and or load
        :type sws_term: uw_sws.term
        """

        def sws_to_utc(dt):
            if isinstance(dt, date):
                # convert date to datetime
                dt = datetime.combine(dt, datetime.min.time())
                SWS_TIMEZONE.localize(dt)
                return dt.astimezone(timezone.utc)

        # get/create model for the term
        term, created = \
            Term.objects.get_or_create(sis_term_id=sws_term.canvas_sis_id())
        if created:
            # add current term info for course
            term.sis_term_id = sws_term.canvas_sis_id()
            term.year = sws_term.year
            term.quarter = sws_term.quarter
            term.label = sws_term.term_label()
            term.last_day_add = sws_to_utc(sws_term.last_day_add)
            term.last_day_drop = sws_to_utc(sws_term.last_day_drop)
            term.first_day_quarter = sws_to_utc(sws_term.first_day_quarter)
            term.census_day = sws_to_utc(sws_term.census_day)
            term.last_day_instruction = \
                sws_to_utc(sws_term.last_day_instruction)
            term.grading_period_open = sws_to_utc(sws_term.grading_period_open)
            term.aterm_grading_period_open = \
                sws_to_utc(sws_term.aterm_grading_period_open)
            term.grade_submission_deadline = \
                sws_to_utc(sws_term.grade_submission_deadline)
            term.last_final_exam_date = \
                sws_to_utc(sws_term.last_final_exam_date)
            term.save()
        return term, created


class Term(models.Model):

    objects = TermManager()
    sis_term_id = models.TextField(null=True)
    year = models.IntegerField(null=True)
    quarter = models.TextField(null=True)
    label = models.TextField(null=True)
    last_day_add = models.DateField(null=True)
    last_day_drop = models.DateField(null=True)
    first_day_quarter = models.DateField(null=True)
    census_day = models.DateField(null=True)
    last_day_instruction = models.DateField(null=True)
    grading_period_open = models.DateTimeField(null=True)
    aterm_grading_period_open = models.DateTimeField(null=True)
    grade_submission_deadline = models.DateTimeField(null=True)
    last_final_exam_date = models.DateTimeField(null=True)

    @property
    def term_number(self):
        return utilities.get_term_number(self.quarter)


class Adviser(models.Model):

    is_active = models.BooleanField(null=True)
    is_dept_adviser = models.BooleanField(null=True)
    full_name = models.TextField(null=True)
    pronouns = models.TextField(null=True)
    email_address = models.TextField(null=True)
    phone_number = models.TextField(null=True)
    uwnetid = models.TextField(null=True)
    regid = models.TextField(null=True)
    program = models.TextField(null=True)
    booking_url = models.TextField(null=True)
    metadata = models.TextField(null=True)
    timestamp = models.DateTimeField(null=True)


class Major(models.Model):
    major_abbr_code = models.TextField(null=True)
    major_name = models.TextField(null=True)
    major_full_name = models.TextField(null=True)
    major_short_name = models.TextField(null=True)


class Student(models.Model):
    student_number = models.BigIntegerField(unique=True)
    uw_net_id = models.TextField(null=True)
    student_name = models.TextField(null=True)
    birthdate = models.DateField(null=True)
    student_email = models.TextField(null=True)
    external_email = models.TextField(null=True)
    local_phone_number = models.TextField(null=True)
    gender = models.TextField(null=True)
    gpa = models.TextField(null=True)
    total_credits = models.TextField(null=True)
    campus_desc = models.TextField(null=True)
    class_desc = models.TextField(null=True)
    enrollment_status = models.TextField(null=True)
    adviser = models.ManyToManyField(Adviser)
    intended_major = models.ManyToManyField(
        Major, related_name="intended_major")  # edited by compass
    major = models.ManyToManyField(Major, related_name="major")
