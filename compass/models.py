# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class User(models.Model):
    uwnetid = models.TextField()
    uwregid = models.TextField()


class Student(models.Model):
    system_key = models.TextField()


class ContactType(models.Model):
    label = models.TextField()


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    label = models.TextField()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField()
    actions = models.TextField()
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
