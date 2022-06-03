# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from simple_history.models import HistoricalRecords


class AppUser(models.Model):
    """
    Authenticated user
    """
    uwnetid = models.CharField(unique=True, max_length=50)
    uwregid = models.CharField(unique=True, max_length=50)

    # A user's Group affiliation is derived at login via GWS Groups. A GWS
    # group key is generated using the <access_id>. It is important to note
    # that UW Group memberships are managed externally from the Compass app.

    class Meta:
        indexes = [
            models.Index(fields=['uwnetid']),
            models.Index(fields=['uwregid']),
        ]


class Student(models.Model):
    system_key = models.CharField(unique=True, max_length=50)
    programs = models.ManyToManyField('Program')

    class Meta:
        indexes = [
            models.Index(fields=['system_key']),
        ]


class AccessGroupManager(models.Manager):

    @property
    def access_group_ids(self):
        return list(
            super().get_queryset().values_list('access_group_id', flat=True))


class AccessGroup(models.Model):
    """
    AccessGroups manage their Program, ContactTopic, and ContactType
    lists. AccessGroup membership is defined externally but determined for a
    AppUser via a request to the GWS at login.
    """

    objects = AccessGroupManager()

    name = models.CharField(unique=True, max_length=50)
    access_group_id = models.CharField(unique=True, max_length=50)
    programs = models.ManyToManyField('Program')
    contact_topics = models.ManyToManyField('ContactTopic')

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Departmental/Group Program (e.g. CAMP, TRIO, SSS, Champions, IC Eligible)
    """
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Contact with a student
    """
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField()
    actions = models.TextField()
    contact_type = models.ForeignKey('ContactType', on_delete=models.CASCADE)
    contact_topics = models.ManyToManyField('ContactTopic')
    # contact history fields
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey('AppUser', on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.author

    @_history_user.setter
    def _history_user(self, value):
        self.author = value


class ContactType(models.Model):
    """
    Type of Contact
    """
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class ContactTopic(models.Model):
    """
    Topic discussed in a Contact
    """
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name
