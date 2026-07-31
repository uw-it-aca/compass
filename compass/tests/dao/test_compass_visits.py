# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0



from django.core.exceptions import ImproperlyConfigured
from restclients_core.exceptions import DataFailureException

from compass.dao.compass_visits import (
    admin_create_visit,
    admin_delete_visit,
    admin_update_visit,
    get_admin_visit_list,
    get_compass_visits_access_group,
    get_visit_options,
    get_visits_for_student,
)
from compass.models import AccessGroup
from compass.tests import CompassTestCase


class CompassVisitsDaoTest(CompassTestCase):
    def setUp(self):
        super().setUp()
        ag = AccessGroup(name="OMAD", access_group_id="u_astra_group1")
        ag.save()

    def test_visits_for_student(self):
        visits = get_visits_for_student("javerage")
        self.assertIsNotNone(visits)
        self.assertEqual(len(visits), 2)
        self.assertEqual(visits[0].id, 1)
        self.assertEqual(visits[0].program_area, "Program Area 3")

        visits = get_visits_for_student("jnovisits")
        self.assertIsNotNone(visits)
        self.assertEqual(len(visits), 0)

    def test_get_admin_visit_list(self):
        visits = get_admin_visit_list()
        self.assertIsNotNone(visits)
        self.assertEqual(len(visits['pending_verification']), 7)
        self.assertEqual(len(visits['by_programarea']), 2)
        self.assertEqual(len(visits['by_programarea']['Program Area 2']), 1)
        self.assertEqual(len(visits['by_programarea']['Program Area 3']), 2)

    def test_get_visit_options(self):
        options = get_visit_options('9136CCB8F66711D5BE060004AC494FFE')
        self.assertIsNotNone(options)
        self.assertIn('program_areas', options)
        self.assertIn('tutoring_options', options)
        self.assertIn('writing_services', options)
        self.assertEqual(len(options['program_areas']), 4)
        self.assertEqual(len(options['tutoring_options']), 3)
        self.assertEqual(len(options['writing_services']), 2)
        self.assertEqual(options['program_areas'][0]['id'], 1)
        self.assertEqual(options['program_areas'][0]['name'],
                         'Program Area 1')

    def test_admin_create_visit(self):
        visit_data = {
            "student_syskey": "000043870",
            "program_area": "1",
            "tutoring_option": "1",
            "writing_service": "1"
        }
        with self.assertRaises(DataFailureException):
            # will fail because the mock dao doesn't support creating visits
            admin_create_visit(visit_data)

    def test_admin_update_visit(self):
        visit = admin_update_visit(1)
        self.assertIsNotNone(visit)
        self.assertEqual(visit.id, 1)

        with self.assertRaises(DataFailureException):
            admin_update_visit(999)

    def test_admin_delete_visit(self):
        response = admin_delete_visit(1)
        self.assertIsNotNone(response)
        self.assertEqual(response.status, 200)

        with self.assertRaises(DataFailureException):
            admin_delete_visit(999)

    def test_get_compass_visits_access_group(self):
        access_group = get_compass_visits_access_group()
        self.assertIsNotNone(access_group)
        self.assertEqual(access_group.name, "OMAD")
        with self.settings(COMPASS_VISITS_ACCESS_GROUP_NAME=None), self.assertRaises(ImproperlyConfigured):
            get_compass_visits_access_group()
        with self.settings(COMPASS_VISITS_ACCESS_GROUP_NAME="OTHER_GROUP"), self.assertRaises(ImproperlyConfigured):
            get_compass_visits_access_group()
