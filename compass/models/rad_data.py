# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.db import models
from compass.models import Student


class FilesProcessed(models.Model):
    """
    Model to track files that have been processed by the RAD system
    """
    file_name = models.CharField(max_length=255)
    processed_date = models.DateTimeField(auto_now_add=True)
    week = models.ForeignKey('RADWeek', on_delete=models.CASCADE)


class DataPoint(models.Model):
    """
    Model to store RAD scores per student, week, course
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    week = models.ForeignKey('RADWeek', on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    activity_score = models.FloatField()
    assignment_score = models.FloatField()
    grade_score = models.FloatField()
    prediction_score = models.FloatField()
    signin_score = models.FloatField()


class RADWeek(models.Model):
    year = models.IntegerField()
    quarter = models.CharField(max_length=255)
    week = models.IntegerField()

    @staticmethod
    def get_week_from_term_date():
        pass
