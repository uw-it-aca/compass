# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections
from django.apps import apps


class Command(BaseCommand):

    def create_person_models(self):
        unmanaged_models = [m for m in apps.get_models() if (
            m._meta.app_label == 'uw_person_client' and
            m._meta.managed is False)]

        connection = connections['uw_person']
        existing_tables = connection.introspection.table_names()

        with connection.schema_editor() as schema_editor:
            for model in unmanaged_models:
                if model._meta.db_table not in existing_tables:
                    schema_editor.create_model(model)

    def handle(self, *args, **options):
        self.create_person_models()

        # Load uw_person data
        for fixture in [
                'person.json', 'employee.json', 'term.json', 'major.json',
                'student.json', 'adviser.json', 'transfer.json',
                'transcript.json', 'hold.json', 'degree.json', 'sport.json']:
            call_command('loaddata', fixture, '--database', 'uw_person',
                         '--app', 'uw_person_client')

        # Load compass data
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
