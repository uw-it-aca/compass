# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from compass.admin import AccessGroupAdminModel, admin_site
from compass.models import (
    AccessGroup,
    Affiliation,
    ContactType,
    EligibilityType,
    VisitType,
)


class AccessGroupAdminActionTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.model_admin = AccessGroupAdminModel(AccessGroup, admin_site)
        self.source_group = AccessGroup.objects.create(
            name="Source Group",
            access_group_id="u_test_source",
        )
        self.target_group = AccessGroup.objects.create(
            name="Target Group",
            access_group_id="u_test_target",
        )

    def _request_with_session(self, path="/admin/", data=None):
        request = self.request_factory.post(path, data=data or {})
        request.session = {}
        request.user = AnonymousUser()
        return request

    def test_action_requires_single_target_group(self):
        request = self._request_with_session(data={})

        with patch.object(self.model_admin, "message_user") as message_user:
            response = self.model_admin.copy_from_access_group(
                request,
                AccessGroup.objects.filter(id__in=[
                    self.source_group.id,
                    self.target_group.id,
                ]),
            )

        self.assertIsNone(response)
        message_user.assert_called_once()
        self.assertIn("Select exactly one target", message_user.call_args.args[1])

    def test_action_renders_confirmation_template(self):
        request = self._request_with_session(
            data={
                "action": "copy_from_access_group",
                "_selected_action": [str(self.target_group.id)],
            },
        )

        response = self.model_admin.copy_from_access_group(
            request,
            AccessGroup.objects.filter(id=self.target_group.id),
        )

        self.assertEqual(response.template_name,
                         "admin/compass/accessgroup/copy_from_access_group.html")
        self.assertEqual(response.context_data["target_group"], self.target_group)
        source_choices = list(response.context_data["source_group_choices"])
        self.assertEqual(source_choices, [self.source_group])

    def test_action_copies_selected_models_and_skips_duplicates(self):
        Affiliation.objects.create(
            access_group=self.source_group,
            name="Alpha Program",
            editable=True,
            active=True,
        )
        Affiliation.objects.create(
            access_group=self.source_group,
            name="Shared Program",
            editable=False,
            active=False,
        )
        Affiliation.objects.create(
            access_group=self.target_group,
            name="Shared Program",
            editable=True,
            active=True,
        )

        EligibilityType.objects.create(
            access_group=self.source_group,
            name="FAFSA",
            editable=False,
        )

        VisitType.objects.create(
            access_group=self.source_group,
            name="Drop-In Lab",
            editable=False,
        )

        request = self._request_with_session(
            data={
                "apply": "1",
                "source_access_group": str(self.source_group.id),
                "copy_affiliations": "on",
                "copy_eligibility_types": "on",
                "copy_visit_types": "on",
            },
        )

        with patch.object(self.model_admin, "message_user") as message_user:
            response = self.model_admin.copy_from_access_group(
                request,
                AccessGroup.objects.filter(id=self.target_group.id),
            )

        self.assertIsNone(response)

        self.assertTrue(
            Affiliation.objects.filter(
                access_group=self.target_group,
                name="Alpha Program",
                active=True,
                editable=True,
            ).exists()
        )
        self.assertEqual(
            Affiliation.objects.filter(
                access_group=self.target_group,
                name="Shared Program",
            ).count(),
            1,
        )
        self.assertTrue(
            EligibilityType.objects.filter(
                access_group=self.target_group,
                name="FAFSA",
                editable=False,
            ).exists()
        )
        self.assertTrue(
            VisitType.objects.filter(
                access_group=self.target_group,
                name="Drop-In Lab",
                editable=False,
            ).exists()
        )

        message_user.assert_called_once()
        message = message_user.call_args.args[1]
        self.assertIn("Affiliations: created=1, skipped=1, conflicts=0", message)
        self.assertIn(
            "Eligibility Types: created=1, skipped=0, conflicts=0",
            message,
        )
        self.assertIn(
            "Visit Types: created=1, skipped=0, conflicts=0",
            message,
        )

    def test_action_reports_slug_conflict(self):
        ContactType.objects.create(
            access_group=self.source_group,
            name="Alpha Beta",
            editable=True,
            active=True,
        )
        ContactType.objects.create(
            access_group=self.target_group,
            name="Alpha-Beta",
            editable=True,
            active=True,
        )

        request = self._request_with_session(
            data={
                "apply": "1",
                "source_access_group": str(self.source_group.id),
                "copy_contact_types": "on",
            },
        )

        with patch.object(self.model_admin, "message_user") as message_user:
            response = self.model_admin.copy_from_access_group(
                request,
                AccessGroup.objects.filter(id=self.target_group.id),
            )

        self.assertIsNone(response)
        self.assertFalse(
            ContactType.objects.filter(
                access_group=self.target_group,
                name="Alpha Beta",
            ).exists()
        )

        message_user.assert_called_once()
        message = message_user.call_args.args[1]
        self.assertIn("Contact Types:", message)
        self.assertIn("conflicts=1", message)
