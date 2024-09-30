# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.storage import RADStorageDao


class TestStorage(TestCase):
    def test_get_term_and_week_from_filename(self):
        filename = "2023-spring-week-6-compass-data.csv"
        year, quarter, week = (
            RADStorageDao.get_year_quarter_week_from_filename(filename))
        self.assertEqual(year, 2023)
        self.assertEqual(quarter, "spring")
        self.assertEqual(week, 6)

    def test_files_list(self):
        dao = RADStorageDao()
        files = dao.get_files_list()
        self.assertEqual(len(files), 10)
        self.assertIn("2023-spring-week-6-compass-data.csv", files)
        self.assertIn("2024-spring-week-5-compass-data.csv", files)
        self.assertIn("2024-spring-week-6-compass-data.csv", files)

    def test_latest_file(self):
        dao = RADStorageDao()
        latest_file = dao.get_latest_file()
        self.assertEqual(latest_file,
                         '2024-spring-week-6-compass-data.csv')

    def test_get_specific_file(self):
        dao = RADStorageDao()
        file = dao.get_file_by_year_quarter_week(2023, 'spring', 6)
        self.assertIsNotNone(file)

    def test_download(self):
        dao = RADStorageDao()
        file = dao.download_from_bucket('2023-spring-week-6-compass-data.csv')
        self.assertIsNotNone(file)
        contents = ("uw_netid,student_no,student_name_lowc,course_code,"
                    "activity,assignments,grades,pred,sign_in,stem,"
                    "incoming_freshman,premajor,eop,international,isso,"
                    "engineering,informatics,campus_code,summer,class_code,"
                    "sport_code")
        self.assertEqual(file.strip(), contents.strip())
