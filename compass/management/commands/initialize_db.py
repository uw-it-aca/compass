# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data/access-groups.json')
        call_command('loaddata', 'initial_data/programs.json')
        call_command('loaddata', 'initial_data/contact-types.json')
        call_command('loaddata', 'initial_data/contact-topics.json')
