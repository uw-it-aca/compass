# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from azure.storage.blob import ContainerClient
from django.conf import settings
import dateparser


class AzureStorageDAO:
    """
    Data Access Object for Azure Storage.
    This class provides methods to interact with Azure Storage services.
    """

    sas_url = getattr(settings, 'AZURE_BLOB_STORAGE_URL', None)
    client = None

    def __init__(self):
        """
        Initializes the AzureStorageDAO
        """
        self.client = ContainerClient.from_container_url(self.sas_url)

    def list_blob_names(self):
        """
        Lists all blobs in the Azure Storage container.
        Returns:
            list: A list of blob names.
        """
        blob_names = []
        for blob in self.client.list_blobs():
            blob_names.append(blob.name)
        return blob_names

    def get_blob(self, blob_name):
        """
        Retrieves a specific blob from the Azure Storage container.
        Args:
            blob_name (str): The name of the blob to retrieve.
        Returns:
            String: The contents of the blob.
        """
        return (self.client.get_blob_client(blob_name)
                .download_blob(encoding='UTF-8').readall())

    def get_most_recent_filename(self):
        """
        Retrieves the most recent blob from the Azure Storage container,
        based on the date present in the filename.
        eg: predictions/predictions_2025-11-17.csv

        Returns:
            String: The filename of the most recent blob.
        """
        latest_filename = None
        latest_date = None
        file_list = self.list_blob_names()
        for filename in file_list:
            try:
                date_str = filename.split('_')[1].split('.')[0]
                file_date = dateparser.parse(date_str)
                if latest_date is None or file_date > latest_date:
                    latest_date = file_date
                    latest_filename = filename
            except (IndexError, ValueError, TypeError):
                continue

        return latest_filename

    def get_latest_file(self):
        """
        Return latest Compass predictions file in bucket
        """
        filename = self.get_most_recent_filename()
        if filename is not None:
            return self.get_blob(filename)
        raise FileNotFoundError("No valid prediction files found in storage.")
