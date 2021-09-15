# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao import EDWClientDAO
from compass.models import Term
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = ("Loads enrolled students into the Compass DB.")

    def add_arguments(self, parser):
        # use current term as the default
        term, _ = Term.objects.get_or_create_term_from_sis_term_id()
        default_sis_term_id = term.sis_term_id
        parser.add_argument("--sis_term_id",
                            type=str,
                            help=("Term to run job for."),
                            default=default_sis_term_id)

    def handle(self, *args, **options):
        sis_term_id = options["sis_term_id"]
        EDWClientDAO().load_enrolled_students(sis_term_id)
