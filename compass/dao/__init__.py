# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from datetime import datetime, timezone

from django.conf import settings
from uw_sws.dao import SWS_TIMEZONE, sws_now


def current_datetime():
    override_dt = getattr(settings, "CURRENT_DATETIME_OVERRIDE", None)
    if override_dt is not None:
        return datetime.strptime(override_dt, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=SWS_TIMEZONE)
    else:
        return sws_now()


def current_datetime_utc():
    return current_datetime().replace(
        tzinfo=SWS_TIMEZONE).astimezone(timezone.utc)
