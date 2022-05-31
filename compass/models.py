# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from simple_history.models import HistoricalRecords


class Student(models.Model):
    system_key = models.TextField(unique=True)
    programs = models.ManyToManyField('Program')

    class Meta:
        indexes = [
            models.Index(fields=['system_key']),
        ]


class User(models.Model):
    """
    Authenticated user
    """
    uwnetid = models.TextField(unique=True)
    uwregid = models.TextField(unique=True)
    # A user's Group affiliation is derived at login via GWS Groups. A GWS
    # group key is generated using the pattern <access-id-prefix>_<Group.slug>.
    # The <access-id-prefix> value is a stored secret. It is important to note
    # thatUW Group memberships are managed externally from the Compass app.

    class Meta:
        indexes = [
            models.Index(fields=['uwnetid']),
            models.Index(fields=['uwregid']),
        ]


class Group(models.Model):
    """
    Groups manage their Program, ContactTopic, and ContactType
    lists. Group members are defined externally and determined via a
    request to the GWS at login. Every student Contact has both an author User
    and a Group relationship.
    """
    name = models.TextField(unique=True)
    slug = models.TextField(unique=True)
    programs = models.ManyToManyField('Program')
    contact_topics = models.ManyToManyField('ContactTopic')
    contact_types = models.ManyToManyField('ContactType')


class Program(models.Model):
    """
    Departmental/Group Program (e.g. CAMP, TRIO, SSS, Champions, IC Eligible)
    """
    name = models.TextField(unique=True)


class Contact(models.Model):
    """
    Contact with a student
    """
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField()
    actions = models.TextField()
    contact_type = models.ForeignKey('ContactType', on_delete=models.CASCADE)
    contact_topics = models.ManyToManyField('ContactTopic')
    # contact history fields
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey('User', on_delete=models.CASCADE)
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
    name = models.TextField(unique=True)


class ContactTopic(models.Model):
    """
    Topic discussed in a Contact
    """
    name = models.TextField(unique=True)
