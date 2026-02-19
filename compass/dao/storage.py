# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
from django.core.files.storage import default_storage
from compass.models.rad_data import RADWeek
from compass.dao.rad_csv import get_pred_csv_from_json
from logging import getLogger


logger = getLogger(__name__)


class RADStorageDao():
    def get_analytics_file_list(self):
        """
        Returns list canvas-analytics compass data files in the bucket.
        """
        dirs, files = default_storage.listdir("compass_data/")

        filenames = []
        for filename in files:
            if filename.endswith('csv') and "pred-proba" not in filename:
                filenames.append(filename)

        logger.info(f"Found the following bucket files: "
                    f"{','.join(filenames)}")
        return filenames

    def get_pred_file_list(self):
        """
        Returns list of prediction files in the bucket.
        """
        dirs, files = default_storage.listdir("prediction_data/")

        filenames = []
        for filename in files:
            if filename.endswith('_predictions.csv'):
                filenames.append(filename)

        logger.info(f"Found the following prediction files: "
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
        filename = (f"compass_data/"
                    f"{year}-{quarter}-week-{week}-compass-data.csv")
        return self.download_from_bucket(filename)

    def write_pred_file(self, content, override_datetime=None):
        """
        Writes prediction file content to the bucket.
        File name set to current timestamp yyyy-mm-dd-HHMMSS_predictions.csv

        :param content: Content to upload
        :type content: str
        :param override_datetime: Optional datetime to use for timestamp
        :type override_datetime: datetime.datetime
        """
        now = override_datetime or datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H%M%S")
        filename = f"prediction_data/{timestamp}_predictions.csv"
        csv_content = get_pred_csv_from_json(content)
        with default_storage.open(filename, mode='wb') as f:
            f.write(csv_content.encode('utf-8'))

    def get_latest_pred_file(self):
        """
        Returns the latest prediction file available in the bucket.
        """
        try:
            dirs, file_list = default_storage.listdir("prediction_data/")
            files = []
            for filename in file_list:
                try:
                    timestamp_str = filename.split("_predictions.csv")[0]
                    timestamp = datetime.datetime.strptime(
                        timestamp_str, "%Y-%m-%d-%H%M%S")
                    data = {"timestamp": timestamp, "gcs_file": filename}
                    files.append(data)
                except ValueError:
                    logger.warning(
                        f"Unable to parse prediction file name: {filename}")
            files.sort(
                   key=lambda i: i['timestamp'],
                   reverse=True)
            if files:
                filename = files[0]['gcs_file']
                url_key = f"prediction_data/{filename}"
                return filename, self.download_from_bucket(url_key)
        except FileNotFoundError:
            logger.warning("No prediction files found in bucket")
            return None, None

    def get_latest_analytics_file(self):
        """
        Return latest Compass RAD file in bucket
        """
        files = []
        for filename in self.get_analytics_file_list():
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
        logger.info(f"Downloading {url_key}")
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
