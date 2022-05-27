# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class ContactType(models.Model):
    label = models.TextField(unique=True)


class Topic(models.Model):
    label = models.TextField(unique=True)


class Group(models.Model):
    label = models.TextField(unique=True)
    slug = models.TextField(unique=True)
    topics = models.ManyToManyField(Topic)
    contact_types = \
        models.ManyToManyField(ContactType)


class User(models.Model):
    uwnetid = models.TextField(unique=True)
    uwregid = models.TextField(unique=True)
    group = models.ManyToManyField(Group)

    class Meta:
        indexes = [
            models.Index(fields=['uwnetid']),
            models.Index(fields=['uwregid']),
        ]


class Student(models.Model):
    system_key = models.TextField(unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['system_key']),
        ]


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField()
    actions = models.TextField()
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
