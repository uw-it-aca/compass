# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch

from compass.models.rad_data import RADImport, RADWeek
from compass.tests import ApiTest


class RetentionPageDataViewTest(ApiTest):

    def _set_support_auth(self, netid='jsupport'):
        self._set_user(netid)
        self._set_group('u_test_group')

    def _create_week_and_import(self, year=2024, quarter='spring', week=5):
        rad_week = RADWeek.get_or_create_week(year=year, quarter=quarter,
                                              week=week)
        rad_import = RADImport.objects.create(week=rad_week)
        return rad_week, rad_import

    @patch('compass.views.support.retention.RADStorageDao')
    @patch('compass.views.support.retention.RADWeek')
    def test_page_data_shape(self, mock_week_cls, mock_storage_cls):
        mock_week_cls.get_most_recent_week.return_value = None
        mock_storage_cls.return_value.get_analytics_file_list.side_effect = Exception
        mock_storage_cls.return_value.get_pred_file_list.side_effect = Exception

        self._set_support_auth()
        response = self.get_response('retention_admin_page_data')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('imports', data)
        self.assertIn('alert_data', data)
        self.assertIn('file_data', data)
        self.assertIn('prediction_files', data)

    @patch('compass.views.support.retention.RADStorageDao')
    def test_page_data_imports_serialized(self, mock_storage_cls):
        mock_storage_cls.return_value.get_analytics_file_list.side_effect = Exception
        mock_storage_cls.return_value.get_pred_file_list.side_effect = Exception

        rad_week, rad_import = self._create_week_and_import()

        self._set_support_auth()
        response = self.get_response('retention_admin_page_data')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['imports']), 1)
        imp = data['imports'][0]
        self.assertEqual(imp['id'], rad_import.id)
        self.assertEqual(imp['year'], rad_week.year)
        self.assertEqual(imp['quarter'], rad_week.quarter)
        self.assertEqual(imp['week'], rad_week.week)
        self.assertIn('import_status', imp)

    @patch('compass.views.support.retention.RADStorageDao')
    @patch('compass.views.support.retention.RADWeek')
    def test_page_data_file_data_none_on_storage_error(self, mock_week_cls,
                                                        mock_storage_cls):
        mock_week_cls.get_most_recent_week.return_value = None
        mock_storage_cls.return_value.get_analytics_file_list.side_effect = Exception(
            'GCS unavailable')
        mock_storage_cls.return_value.get_pred_file_list.side_effect = Exception(
            'GCS unavailable')

        self._set_support_auth()
        response = self.get_response('retention_admin_page_data')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsNone(data['file_data'])
        self.assertIsNone(data['prediction_files'])

    @patch('compass.views.support.retention.RADStorageDao')
    @patch('compass.views.support.retention.RADWeek')
    def test_page_data_requires_support_group(self, mock_week_cls,
                                              mock_storage_cls):
        mock_week_cls.get_most_recent_week.return_value = None
        mock_storage_cls.return_value.get_analytics_file_list.side_effect = Exception
        mock_storage_cls.return_value.get_pred_file_list.side_effect = Exception

        # No auth at all
        response = self.get_response('retention_admin_page_data')
        self.assertIn(response.status_code, [302, 403])

    @patch('compass.views.support.retention.RADStorageDao')
    @patch('compass.views.support.retention.RADWeek')
    def test_page_data_wrong_group_denied(self, mock_week_cls, mock_storage_cls):
        mock_week_cls.get_most_recent_week.return_value = None
        mock_storage_cls.return_value.get_analytics_file_list.side_effect = Exception
        mock_storage_cls.return_value.get_pred_file_list.side_effect = Exception

        self._set_user('jsupport')
        self._set_group('u_wrong_group')

        response = self.get_response('retention_admin_page_data')
        self.assertIn(response.status_code, [302, 403])
