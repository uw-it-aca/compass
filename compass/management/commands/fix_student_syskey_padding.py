# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.db.models.functions import Length
from compass.models import Contact, Student, StudentAffiliation, \
    Visit, StudentEligibility


class Command(BaseCommand):
    help = "Fixes syskeys with no leading zero padding"

    def handle(self, *args, **options):
        students_to_fix = Student.objects\
            .annotate(syskey_len=Length('system_key'))\
            .filter(syskey_len__lt=9)
        for student in students_to_fix:
            padded_syskey = student.system_key.zfill(9)
            try:
                padded_student = \
                    Student.objects.filter(system_key=padded_syskey).get()
                try:
                    contacts = Contact.objects.filter(student=student)
                    for contact in contacts:
                        contact.student = padded_student
                    Contact.objects.bulk_update(contacts, ['student'])
                except Contact.DoesNotExist:
                    pass
                try:
                    affils = StudentAffiliation.objects.filter(student=student)
                    for affil in affils:
                        affil.student = padded_student
                    StudentAffiliation.objects.bulk_update(affils, ['student'])
                except StudentAffiliation.DoesNotExist:
                    pass
                try:
                    visits = Visit.objects.filter(student=student)
                    for visit in visits:
                        visit.student = padded_student
                    Visit.objects.bulk_update(visits, ['student'])
                except Visit.DoesNotExist:
                    pass
                try:
                    eligs = StudentEligibility.objects.filter(student=student)
                    for elig in eligs:
                        elig.student = padded_student
                    StudentEligibility.objects.bulk_update(eligs, ['student'])
                except StudentEligibility.DoesNotExist:
                    pass
                student.delete()

            except Student.DoesNotExist:
                student.system_key = padded_syskey
                student.save()
