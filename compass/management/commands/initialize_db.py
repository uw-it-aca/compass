# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data/access-groups.json')
        call_command('loaddata', 'initial_data/affiliations.json')
        call_command('loaddata', 'initial_data/cohorts.json')
        call_command('loaddata', 'initial_data/student.json')
        call_command('loaddata', 'initial_data/app-user.json')
        call_command('loaddata', 'initial_data/student-affiliations.json')
        call_command('loaddata', 'initial_data/contact-types.json')
        call_command('loaddata', 'initial_data/contact-methods.json')
        call_command('loaddata', 'initial_data/contact-topics.json')
        call_command('loaddata', 'initial_data/visit-types.json')
        call_command('loaddata', 'initial_data/visit.json')
        call_command('loaddata', 'initial_data/eligibility-types.json')
        call_command('loaddata', 'initial_data/specialprogram.json')
