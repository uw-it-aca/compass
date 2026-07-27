# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json

from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.authtoken.models import Token

from compass.models import AccessGroup, Contact, OMADContactQueue
from compass.tests import CompassTestCase


class TestOMADContactProcessing(CompassTestCase):
    API_TOKEN = None

    def setUp(self):
        super().setUp()
        AccessGroup(name="OMAD", access_group_id="u_astra_group1").save()
        user = User.objects.create_user(username='testuser', password='12345')
        token = Token.objects.create(user=user)
        self.API_TOKEN = token.key

    def test_success(self):
        # Create a contact queue entry
        test_body = {
            "adviser_netid": "javerage",
            "student_systemkey": "001234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass",
            "trans_id": 1234567890
        }
        OMADContactQueue.objects.create(json=json.dumps(test_body))
        call_command('process_omad_contacts')
        self.assertEqual(OMADContactQueue.objects.count(), 0)
        self.assertEqual(Contact.objects.count(), 1)

    def test_failure(self):
        test_body = {
            "adviser_netid": "javerage123",
            "student_systemkey": "001234567",
            "contact_type": "appointment",
            "checkin_date": "2012-01-19 17:21:00 PDT",
            "source": "Compass",
            "trans_id": 1234567890
        }
        OMADContactQueue.objects.create(json=json.dumps(test_body))
        call_command('process_omad_contacts')
        self.assertEqual(OMADContactQueue.objects.count(), 1)
        self.assertEqual(Contact.objects.count(), 0)
        # don't reprocess without flag
        call_command('process_omad_contacts')
        contact = OMADContactQueue.objects.all()[0]
        self.assertEqual(contact.processing_attempts, 1)
        self.assertEqual(contact.processing_error,
                         "PersonNotFoundException('javerage123')")

        # reprocess with flag
        call_command('process_omad_contacts', reprocess=True)
        contact = OMADContactQueue.objects.all()[0]
        self.assertEqual(contact.processing_attempts, 2)
