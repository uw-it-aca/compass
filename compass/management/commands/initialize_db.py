# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.core.management import call_command
from compass.models import AffiliationGroup, Affiliation


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data/access-groups.json')
        call_command('loaddata', 'initial_data/affiliation-groups.json')
        call_command('loaddata', 'initial_data/affiliations.json')
        # add affiliationGroup exclusivity_group now that affiliation FKs exist
        ag = AffiliationGroup.objects.get(pk=1)
        ag.exclusivity_group.add(Affiliation.objects.get(pk=1))
        ag.exclusivity_group.add(Affiliation.objects.get(pk=2))
        call_command('loaddata', 'initial_data/cohorts.json')
        call_command('loaddata', 'initial_data/student.json')
        call_command('loaddata', 'initial_data/student-affiliations.json')
        call_command('loaddata', 'initial_data/contact-types.json')
        call_command('loaddata', 'initial_data/contact-methods.json')
        call_command('loaddata', 'initial_data/contact-topics.json')
