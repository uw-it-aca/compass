# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from compass.models.rad_data import (RADWeek,
                                     CourseAnalyticsScores,
                                     StudentAlertStatus)
from logging import getLogger

logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Generates alert status for current week"

    def handle(self, *args, **options):
        current_week = RADWeek.get_most_recent_week()
        if current_week is None:
            logger.error("No current week found")
            return

        # clear existing predictions
        StudentAlertStatus.objects.all().delete()

        score_data = (
            CourseAnalyticsScores.get_all_predections_for_week(current_week))
        alert_objects = []
        for uwnetid in score_data:
            alert_objects.append(StudentAlertStatus(
                uwnetid=uwnetid,
                alert_status=StudentAlertStatus.get_alert_class_from_scores(
                    score_data[uwnetid])
            ))
        StudentAlertStatus.objects.bulk_create(alert_objects)
