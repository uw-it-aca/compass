# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
from compass.models import (
    AccessGroup, Student, StudentAffiliation, Affiliation, Cohort)
from datetime import datetime
from pytz import timezone
import string
import argparse
import pytz
import sys
import csv
import re


class UnknownLegacyAssociation(Exception):
    pass


class Command(BaseCommand):
    help = ("load compass legacy program data from csv dump of affiliation",
            " and affiliation_association table")

    def add_arguments(self, parser):
        parser.add_argument('affiliations')
        parser.add_argument('affiliation_associations')

    def handle(self, *args, **options):
        self.uw_person = UWPersonClient()
        self.access_group = AccessGroup.objects.get(name='OMAD')

        self.load_affiliation_table(options['affiliations'])
        self.load_affiliations(options['affiliation_associations'])

    def _get_affiliation_name(self, affiliation):
        mapping = [
            (['camp'],
             'CAMP', True),
            (['triosss', 'sss'],
             'TRIO SSS', True),
            (['triosssstem'],
             'TRIO SSS-STEM', True),
            (['eip'],
             'EIP', True),
            (['eiplab'],
             'EIP Lab', True),
            (['champions'],
             'Champions', True),
            (['lsamp'],
             'LSAMP', True),
            (['mesa'],
             'MESA', True),
            (['eopscholar'],
             'EOP Scholar', True),
            (['brotherhoodinitiativescholar'],
             'Brotherhood Initiative Scholar', True),
            (['diversityscholar'],
             'Diversity Scholar', True),
            (['mcnairscholar'],
             'McNair Scholar', True),
            (['hscmsp'],
             'HSCMSP', True),
            (['sisterhoodinitiativescholar'],
             'Sisterhood Initiative Scholar', True),
            (['duscholars'],
             'DU Scholars', True),
            (['dadgar/kallascholar'],
             'Dadgar/Kalla Scholar', True),
            (['lsamp'],
             'LSAMP', True),
            (['affiliation6'],
             'Affiliation 6', False),
            (['affiliation5'],
             'Affiliation 5', False),
            (['affiliation4'],
             'Affiliation 4', False),
            (['gearupseattle'],
             'GearupSeattle', False),
            (['reentry'],
             'ReEntry', False),
            (['imsd'],
             'IMSD', False),
            (['wetep'],
             'WeTep', False),
            (['iceligible'],
             'ICEligible', False),
            (['wsas'],
             'WSAS', False),
            (['upwardbound'],
             'UpwardBound', False),
            ([''],
             'Other', False)]

        for legacy, name, active in mapping:
            if self._normal(affiliation) in legacy:
                return name, active

        raise UnknownLegacyAssociation("{} ({})".format(
            affiliation, self._normal(affiliation)))

    def load_affiliation_table(self, filename):

        with open(filename, 'r') as csvfile:
            next(csvfile, None)
            for row in csv.reader(csvfile, delimiter=","):
                try:
                    a = LegacyAffiliation(row)
                    name, active = self._get_affiliation_name(a.affiliation)
                    affiliation = self._get_affiliation(name)
                    if affiliation.active != active:
                        affiliation.active = active
                        affiliation.save()
                except UnknownLegacyAssociation as ex:
                    self._error(
                        'Unknown legacy affiliation: {}'.format(ex))

    def _get_affiliation(self, affiliation):
        affiliation, created = Affiliation.objects.get_or_create(
            access_group=self.access_group, name=affiliation)
        return affiliation

    def load_affiliations(self, filename):
        with open(filename, 'r') as csvfile:
            next(csvfile, None)
            for row in csv.reader(csvfile, delimiter=","):
                a = Association(row)
                student_number = a.student_number.zfill(7)
                try:
                    student = self._get_student(student_number)
                    name, active = self._get_affiliation_name(a.affiliation)
                    affiliation = self._get_affiliation(name)
                    sa = self._get_student_affiliation(student, affiliation)
                    sa.actively_advised = (a.active.lower() in ['yes', ''])

                    sa.date = None
                    date = a.date_modified if a.date_modified else a.date
                    if date:
                        try:
                            sa.date = datetime.strptime(
                                date, '%m/%d/%Y').date()
                        except ValueError:
                            try:
                                sa.date = datetime.strptime(
                                    date, '%m/%d/%y').date()
                            except ValueError:
                                pass

                    sa.save()
                    self._set_cohorts(sa, a.cohort)
                except PersonNotFoundException:
                    self._error(
                        "Person Not Found affiliation {}: {}".format(
                            a.ID, student_number))
                except UnknownLegacyAssociation as ex:
                    self._error(
                        'Unknown legacy affiliation: {}'.format(ex))

    def _set_cohorts(self, student_affiliation, cohorts_list):
        cohort_re = re.compile('^([0-9]+)-([0-9]+)')
        for cohort_string in cohorts_list.split(','):
            cohorts = []
            m = cohort_re.search(cohort_string)
            if m:
                start_year = int('20' + m.group(1) if (
                    int(m.group(1)) < 100) else m.group(1))
                end_year = int('20' + m.group(2) if (
                    int(m.group(2)) < 100) else m.group(2))
                cohort = self._get_cohort(start_year, end_year)
                student_affiliation.cohorts.add(cohort)
                student_affiliation.save()

    def _get_student_affiliation(self, student, affiliation):
        sa, created = StudentAffiliation.objects.get_or_create(
            student=student, affiliation=affiliation)
        return sa

    def _get_student(self, student_number):
        person = self.uw_person.get_person_by_student_number(
            student_number, include_employee=False, include_student=True,
            include_student_transcripts=False, include_student_transfers=False,
            include_student_sports=False, include_student_advisers=False,
            include_student_majors=False, include_student_pending_majors=False,
            include_student_holds=False, include_student_degrees=False)
        student, created = Student.objects.get_or_create(
            system_key=person.student.system_key)
        return student

    def _get_cohort(self, start_year, end_year):
        cohort, created = Cohort.objects.get_or_create(
            start_year=start_year, end_year=end_year)
        return cohort

    def _normal(self, affiliation):
        return affiliation.translate(
            {ord(c): None for c in string.whitespace}).lower()

    def _error(self, msg):
        print(msg, file=sys.stderr)


class LegacyAffiliation(object):
    AFFILIATION_COLUMNS = ["affilationID", "affiliation"]

    def __init__(self, row):
        for i, k in enumerate(self.AFFILIATION_COLUMNS):
            setattr(self, k, row[i].strip())


class Association(object):
    ASSOCIATION_COLUMNS = [
        "ID", "student_number", "affiliation", "cohort",
        "date", "date_modified", "active"]

    def __init__(self, row):
        for i, k in enumerate(self.ASSOCIATION_COLUMNS):
            setattr(self, k, row[i].strip())
