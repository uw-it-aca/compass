# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import logging
from django.core.files.storage import default_storage


def get_term_and_week_from_filename(rad_file_name):
    """
    Extracts term and week from Compass RAD data file name

    For example:

    "compass_data/2021-spring-week-10-compass-data.csv" -> "2021-spring", 10
    """
    try:
        if rad_file_name.startswith("compass_data/"):
            rad_file_name = rad_file_name.split("/")[1]
        parts = rad_file_name.split("-")
        term = f"{parts[0]}-{parts[1]}"
        week = int(parts[3])
    except IndexError:
        raise ValueError(f"Unable to parse RAD file name: {rad_file_name}")
    return term, week


class StorageDao():
    def get_files_list(self, path=''):
        """
        Returns list of file names at the given path.

        :param path: Path to list files at
        :type path: str
        """
        dirs, files = default_storage.listdir(path)

        filenames = []
        for filename in files:
            if filename.endswith('csv'):
                filenames.append(filename)

        logging.debug(f"Found the following bucket files: "
                      f"{','.join(filenames)}")
        return filenames

    def get_latest_file(self):
        """
        Return latest Compass RAD file in bucket
        """
        files = []
        for filename in self.get_files_list():
            sis_term_id, week_num = get_term_and_week_from_filename(filename)
            year = sis_term_id.split("-")[0]
            # TODO: Implement Week.sis_term_to_quarter_number
            quarter_num = 0
            # quarter_num = Week.sis_term_to_quarter_number(sis_term_id)
            data = {"year": year, "quarter_num": quarter_num,
                    "week_num": week_num, "gcs_file": filename}
            files.append(data)
        files.sort(
               key=lambda i: (int(i['year']), int(i['quarter_num']),
                              int(i['week_num'])),
               reverse=True)
        return files[0]["gcs_file"]

    def download_from_bucket(self, url_key):
        """
        Downloads file a given url_key path from the configured bucket.

        :param url_key: Path of the content to upload
        :type url_key: str
        """
        with default_storage.open(url_key, mode='rb') as f:
            content = f.read()
            return content.decode('utf-8')
