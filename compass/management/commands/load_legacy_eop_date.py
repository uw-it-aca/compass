# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
from compass.models import AccessGroup, Student, StudentProgram
from datetime import datetime, date
from pytz import timezone
import string
import argparse
import pytz
import sys
import csv
import re


class Command(BaseCommand):
    help = "load compass SpecialProgram table form legacy EOP_date csv dump"

    def add_arguments(self, parser):
        parser.add_argument('eop_type')

    def handle(self, *args, **options):
        self.uw_person = UWPersonClient()
        self.access_group = AccessGroup.objects.get(name='OMAD')

        self.load_eop_types(options['eop_type'])

    def load_eop_types(self, filename):
        seen = {}
        with open(filename, 'r') as csvfile:
            next(csvfile, None)
            for row in csv.reader(csvfile, delimiter=","):
                a = EOP_Type(row)
                student_number = a.student_number.zfill(7)

                try:
                    seen[student_number] += 1
                except KeyError:
                    seen[student_number] = 1

                try:
                    if False:
                        student, pds_student = self._get_student(student_number)
                        program_code = int(pds_student.special_program_code)
                    else:
                        program_code = 1
                except ValueError:
                    self._error(
                        f"Malformed program code for {student_number}: "
                        f"{student.special_program_code}")
                except PersonNotFoundException:
                    self._error(
                        f"No pds record for student id {student_number}")

                if not a.EOP_Date or len(a.EOP_Date) == 0:
                    if seen[student_number] > 1:
                        print(f"{student_number} (seen {seen[student_number]} "
                              f"times) missing EOP_Date {modified_date}")

                if not a.date_modified or len(a.date_modified) == 0:
                    print(f"{student_number} (seen {seen[student_number]} "
                          f"times) missing modified date")

                date = datetime.strptime(a.EOP_Date, '%Y-%m-%d').date() if (
                    a.EOP_Date and len(a.EOP_Date)) else None
                modified_date = datetime.fromisoformat(a.date_modified) if (
                    a.date_modified and len(a.date_modified) > 1) else None

                sp, created = StudentProgram.objects.uppate_or_create(
                    student=student, access_group=self.access_group,
                    program_code=program_code, defaults={
                        'date': date, 'modified_date': modified_date})

                print(f"{'Stored' if created else 'Updated'} "
                      f"{student_number} ({student.system_key}) with "
                      f"{program_code} on {date} modified {modified_date}")

    def _get_student(self, student_number):
        person = self.uw_person.get_person_by_student_number(
            student_number, include_employee=False, include_student=True,
            include_student_transcripts=False, include_student_transfers=False,
            include_student_sports=False, include_student_advisers=False,
            include_student_majors=False, include_student_pending_majors=False,
            include_student_holds=False, include_student_degrees=False)
        student, created = Student.objects.get_or_create(
            system_key=person.student.system_key)
        return student, person.student

    def _normal(self, affiliation):
        return affiliation.translate(
            {ord(c): None for c in string.whitespace}).lower()

    def _error(self, msg):
        print(msg, file=sys.stderr)


class EOP_Type(object):
    ASSOCIATION_COLUMNS = [
        "student_number", "Is_EOP", "EOP_Date", "EOP_Name", "date_modified"]

    def __init__(self, row):
        for i, k in enumerate(self.ASSOCIATION_COLUMNS):
            setattr(self, k, row[i].strip())
