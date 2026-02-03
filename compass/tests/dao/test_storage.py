# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import datetime
from django.test import TestCase
from django.test.utils import override_settings
from compass.dao.storage import RADStorageDao


class TestStorage(TestCase):
    # def test_get_term_and_week_from_filename(self):
    #     filename = "2023-spring-week-6-compass-data.csv"
    #     year, quarter, week = (
    #         RADStorageDao.get_year_quarter_week_from_filename(filename))
    #     self.assertEqual(year, 2023)
    #     self.assertEqual(quarter, "spring")
    #     self.assertEqual(week, 6)

    def test_files_list(self):
        dao = RADStorageDao()
        files = dao.get_analytics_file_list()
        self.assertEqual(len(files), 11)
        self.assertIn("2023-spring-week-6-compass-data.csv", files)
        self.assertIn("2024-spring-week-5-compass-data.csv", files)
        self.assertIn("2024-spring-week-6-compass-data.csv", files)

    def test_latest_file(self):
        dao = RADStorageDao()
        latest_file = dao.get_latest_analytics_file()
        self.assertEqual(latest_file,
                         '2024-spring-week-6-compass-data.csv')

    def test_get_specific_file(self):
        dao = RADStorageDao()
        file = dao.get_file_by_year_quarter_week(2023, 'spring', 6)
        self.assertIsNotNone(file)

    def test_download(self):
        dao = RADStorageDao()
        file = dao.download_from_bucket('compass_data/'
                                        '2023-spring-week-6-compass-data.csv')
        self.assertIsNotNone(file)
        contents = ("uw_netid,student_no,student_name_lowc,course_code,"
                    "activity,assignments,grades,pred,sign_in,stem,"
                    "incoming_freshman,premajor,eop,international,isso,"
                    "engineering,informatics,campus_code,summer,class_code,"
                    "sport_code")
        self.assertEqual(file.strip(), contents.strip())

    @override_settings(STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.memory.InMemoryStorage',
        }
    })
    def test_upload_prediction(self):
        test_datetime = datetime.datetime(2024, 5, 1, 12, 10, 32)
        dao = RADStorageDao()
        content = "uw_netid,prediction\njdoe,True\nasmith,False"
        dao.write_pred_file(content, override_datetime=test_datetime)
        downloaded_content = dao.download_from_bucket(
            'prediction_data/2024-05-01-121032_predictions.csv')
        self.assertEqual(downloaded_content, content)

    def test_get_latest_prediction(self):
        dao = RADStorageDao()
        filename, content = dao.get_latest_pred_file()
        self.assertIsNotNone(content)
        with open('compass/fixtures/storage/prediction_data'
                  '/2025-05-01-121033_predictions.csv') as f:
            expected_content = f.read()
            self.assertEqual(content, expected_content)
