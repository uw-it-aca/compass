# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from userservice.user import UserService
from compass.tests import ApiTest
from compass.models import AccessGroup, AppUser
from unittest.mock import patch


class SpecialProgramAPITest(ApiTest):
    fixtures = [
        'initial_data/access-groups.json',
        'initial_data/app-user.json',
        'initial_data/student.json',
        'initial_data/specialprogram.json',
    ]
    url_kwargs1 = {'systemkey': '532353230'}
    url_kwargs2 = {'systemkey': '123123123'}

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_get(self, mock_is_member):
        response = self.get_response(
            'special_program_view', 'jadviser', kwargs=self.url_kwargs1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('program_date'), '2023-12-31')

        response = self.get_response(
            'special_program_view', 'jadviser', kwargs=self.url_kwargs2)

        self.assertEqual(response.status_code, 404)

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_post(self, mock_is_member):
        data = {
            'special_program': {
                'program_date': '2024-01-01'
            }
        }

        response = self.post_response(
            'special_program_view', 'jadviser', data, kwargs=self.url_kwargs2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('program_date'), '2024-01-01')

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_post_permission_failure(self, mock_is_member):
        data = {
            'special_program': {
                'program_date': '2024-13-33'
            }
        }

        response = self.post_response(
            'special_program_view', data, 'javerage', kwargs=self.url_kwargs1)

        self.assertEqual(response.status_code, 401)

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_post_data_failure(self, mock_is_member):
        data = {
            'special_program': {
                'program_date': '2024-01-01'
            }
        }

        response = self.post_response(
            'special_program_view', 'jadviser', data, kwargs=self.url_kwargs1)

        self.assertEqual(response.status_code, 400)

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_put(self, mock_is_member):
        data = {
            'special_program': {
                'program_date': '2024-02-01'
            }
        }

        response = self.put_response(
            'special_program_view', 'jadviser', data, kwargs=self.url_kwargs1)

        self.assertEqual(response.status_code, 200)

    @patch('compass.dao.group.is_member_of_group', return_value=True)
    def test_delete(self, mock_is_member):
        response = self.delete_response(
            'special_program_view', 'jadviser', kwargs=self.url_kwargs1)

        self.assertEqual(response.status_code, 200)
