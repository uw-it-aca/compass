# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.core.files.storage import default_storage
from compass.models.rad_data import RADWeek
from logging import getLogger


logger = getLogger(__name__)


class RADStorageDao():
    def get_files_list(self, path=''):
        """
        Returns list of file names at the given path.

        :param path: Path to list files at
        :type path: str
        """
        dirs, files = default_storage.listdir(path)

        filenames = []
        for filename in files:
            if filename.endswith('csv') and "pred-proba" not in filename:
                filenames.append(filename)

        logger.info(f"Found the following bucket files: "
                      f"{','.join(filenames)}")
        return filenames

    def get_file_by_year_quarter_week(self, year, quarter, week):
        """
        Returns the file name for the given year, quarter, and week.

        :param year: Year to search for
        :type year: int
        :param quarter: Quarter to search for
        :type quarter: str
        :param week: Week to search for
        :type week: int
        """
        filename = f"{year}-{quarter}-week-{week}-compass-data.csv"
        return self.download_from_bucket(filename)

    def get_pred_file_by_y_q_w(self, year, quarter, week):
        """
        Returns the file name for the given year, quarter, and week.

        :param year: Year to search for
        :type year: int
        :param quarter: Quarter to search for
        :type quarter: str
        :param week: Week to search for
        :type week: int
        """
        # TODO change to per-week stats once analytics team automates that
        filename = f"{year}-{quarter}-pred-proba.csv"
        logger.info(f"Attempting download of file: {filename}")
        return self.download_from_bucket(filename)

    def get_latest_file(self):
        """
        Return latest Compass RAD file in bucket
        """
        files = []
        for filename in self.get_files_list():
            year, quarter, week_num = (
                self.get_year_quarter_week_from_filename(filename))
            quarter_num = RADWeek.get_quarter_number(quarter)
            data = {"year": year, "quarter_num": quarter_num,
                    "week_num": week_num, "gcs_file": filename}
            files.append(data)
        files.sort(
               key=lambda i: (int(i['year']), int(i['quarter_num']),
                              int(i['week_num'])),
               reverse=True)
        return files[0]["gcs_file"]

    @staticmethod
    def download_from_bucket(url_key):
        """
        Downloads file a given url_key path from the configured bucket.

        :param url_key: Path of the content to upload
        :type url_key: str
        """
        with default_storage.open(url_key, mode='rb') as f:
            content = f.read()
            return content.decode('utf-8')

    @staticmethod
    def get_year_quarter_week_from_filename(rad_file_name):
        """
        Extracts term, week and year from Compass RAD data file name

        For example:

        "compass_data/2021-spring-week-10-compass-data.csv"
         -> "2021", "spring", 10
        """
        try:
            if rad_file_name.startswith("compass_data/"):
                rad_file_name = rad_file_name.split("/")[1]
            parts = rad_file_name.split("-")
            year = int(parts[0])
            quarter = parts[1]
            week = int(parts[3])
        except IndexError:
            raise ValueError(f"Unable to parse RAD file name: {rad_file_name}")
        return year, quarter, week
