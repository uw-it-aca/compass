# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from datetime import datetime
from uw_sws.dao import sws_now, SWS_TIMEZONE
import pytz


def current_datetime():
    override_dt = getattr(settings, "CURRENT_DATETIME_OVERRIDE", None)
    if override_dt is not None:
        return datetime.strptime(override_dt, "%Y-%m-%d %H:%M:%S")
    else:
        return sws_now()


def current_datetime_utc():
    return SWS_TIMEZONE.localize(current_datetime()).astimezone(pytz.utc)
