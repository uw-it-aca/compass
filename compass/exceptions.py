# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class OverrideNotPermitted(Exception):
    def __str__(self):
        return "Action not permitted while using admin override"


class InvalidSystemKey(Exception):
    def __str__(self):
        return "system_key is invalid"


class InvalidCSV(Exception):
    def __init__(self, error="Invalid CSV file"):
        self.error = error

    def __str__(self):
        return self.error
