# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from compass.models import OMADContactQueue
from datetime import datetime
import json
from compass.models import (
    AccessGroup, AppUser, Contact, Student)
from logging import getLogger
from compass.dao.contact import (validate_contact_post_data,
                                 pad_student_systemkey)
import traceback
logger = getLogger(__name__)



class Command(BaseCommand):
    help = "process OMAD contacts"

    def add_arguments(self, parser):
        parser.add_argument('--reprocess',
                            action='store_true',
                            help="reprocess all contacts regardless of status")

    def handle(self, *args, **options):
        if options['reprocess']:
            contacts = OMADContactQueue.objects.all()
        else:
            contacts = OMADContactQueue.objects.filter(processing_attempts=0)

        for contact in contacts:
            try:
                self.process_contact(contact)
            except Exception as e:
                logger.exception(f"Error processing contact {contact.id}: {e}")
                contact.processing_attempts += 1
                contact.process_attempted_date = datetime.now()
                contact.processing_error = repr(e)
                contact.stack_trace = traceback.format_exc()
                contact.save()
                continue
            contact.delete()

    @staticmethod
    def process_contact(contact):
        contact_dict = json.loads(contact.json)
        validate_contact_post_data(contact_dict)

        # Get additional objects
        access_group = AccessGroup.objects.by_name("OMAD")
        app_user = AppUser.objects.upsert_appuser(
            contact_dict["adviser_netid"])

        # Parse/format data
        student_systemkey = pad_student_systemkey(
            contact_dict["student_systemkey"])

        student, _ = Student.objects.get_or_create(
            system_key=student_systemkey)

        # create the new contact record
        contact = Contact()
        contact.app_user = app_user
        contact.student = student
        contact.contact_type = contact_dict["contact_type"]
        contact.checkin_date = contact_dict["checkin_date"]
        contact.source = "Checkin"
        try:
            contact.trans_id = contact_dict["trans_id"]
        except KeyError:
            pass
        contact.save()
        contact.access_group.add(access_group)
        logger.info(f"Checkin contact {contact.contact_type} processed for "
                    f"student {student.system_key}")
