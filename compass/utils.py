# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta

STUDENT_NUM_LEN = 7
STUDENT_SYSKEY_LEN = 9


def zfill_or_none(value, length):
    value = str(value).zfill(length) if (
        value and str(value).isdigit()) else None
    if value == '0' * length:
        return None
    return value


def format_system_key(value):
    return zfill_or_none(value, STUDENT_SYSKEY_LEN)


def format_student_number(value):
    return zfill_or_none(value, STUDENT_NUM_LEN)


def weekdays_before(end_date, offset_days=3):
    """
    Adjust a start_date to exclude weekend days from the passed offset_days.
    """
    start_date = end_date
    if offset_days is not None and offset_days > 0:
        start_date = end_date - timedelta(days=offset_days)

    day = start_date
    actual_offset = 1 if (day.weekday() == 6) else 0
    while day < end_date:
        actual_offset += 1
        if day.weekday() >= 5:
            actual_offset += 1
        day = day + timedelta(days=1)

    return end_date - timedelta(days=actual_offset)
