# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


"""
Custom exceptions used by Compass.
"""


class OverrideNotPermitted(Exception):
    def __str__(self):
        return "Action not permitted while using admin override"


class InvalidSystemKey(Exception):
    def __str__(self):
        return "system_ey is invalid"
