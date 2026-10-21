# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import pprint

from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from rest_framework.authtoken.models import TokenProxy

from compass.dao.group import is_admin_user
from compass.models import (
    AccessGroup,
    Affiliation,
    AppUser,
    Contact,
    ContactMethod,
    ContactTopic,
    ContactType,
    EligibilityType,
    OMADContactQueue,
    Student,
    StudentEligibility,
    Visit,
    VisitTutoringOption,
    VisitType,
)


class SAMLAdminSite(admin.AdminSite):
    site_header = 'Compass admin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def has_permission(self, request):
        return is_admin_user(request)

    def login(self, request, extra_context=None):
        if self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        else:
            return HttpResponseRedirect('/not-authorized/')


class AbstractSAMLAdminModel:
    def has_add_permission(self, request):
        return is_admin_user(request)

    def has_change_permission(self, request, obj=None):
        return is_admin_user(request)

    def has_delete_permission(self, request, obj=None):
        return is_admin_user(request)

    def has_module_permission(self, request):
        return is_admin_user(request)


class SAMLAdminModel(AbstractSAMLAdminModel, admin.ModelAdmin):
    pass


class SessionAdminModel(SAMLAdminModel):
    def user(self, obj):
        session_user = obj.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=session_user)
        return user.username

    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')

    _session_data.allow_tags = True
    list_display = ('user', 'session_key', '_session_data', 'expire_date')
    readonly_fields = ('_session_data',)


class AccessGroupAdminModel(SAMLAdminModel):
    actions = ("copy_from_access_group",)

    def _copy_records(self, source_group, target_group, model_class):
        created = 0
        skipped = 0
        conflicts = 0

        source_items = model_class.objects.filter(access_group=source_group)
        for source_item in source_items:
            if model_class.objects.filter(
                    access_group=target_group,
                    name=source_item.name).exists():
                skipped += 1
                continue

            payload = {
                "access_group": target_group,
                "name": source_item.name,
                "editable": source_item.editable,
            }
            if hasattr(source_item, "active"):
                payload["active"] = source_item.active

            try:
                with transaction.atomic():
                    model_class.objects.create(**payload)
                created += 1
            except IntegrityError:
                # Usually a slug collision when the generated slug already exists.
                conflicts += 1

        return created, skipped, conflicts

    def copy_from_access_group(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Select exactly one target Access Group to copy settings into.",
                level="ERROR",
            )
            return None

        target_group = queryset.first()

        if request.POST.get("apply"):
            source_group_id = request.POST.get("source_access_group")
            if not source_group_id:
                self.message_user(
                    request,
                    "Choose a source Access Group.",
                    level="ERROR",
                )
                return None

            try:
                source_group = AccessGroup.objects.get(id=source_group_id)
            except AccessGroup.DoesNotExist:
                self.message_user(
                    request,
                    "Selected source Access Group does not exist.",
                    level="ERROR",
                )
                return None

            if source_group.id == target_group.id:
                self.message_user(
                    request,
                    "Source and target Access Groups must be different.",
                    level="ERROR",
                )
                return None

            model_groups = [
                ("copy_affiliations", "Affiliations", Affiliation),
                ("copy_contact_types", "Contact Types", ContactType),
                ("copy_contact_methods", "Contact Methods", ContactMethod),
                ("copy_contact_topics", "Contact Topics", ContactTopic),
                ("copy_eligibility_types", "Eligibility Types", EligibilityType),
                ("copy_visit_types", "Visit Types", VisitType),
            ]

            selected = [
                (label, model_class)
                for field_name, label, model_class in model_groups
                if request.POST.get(field_name)
            ]

            if not selected:
                self.message_user(
                    request,
                    "Choose at least one settings type to copy.",
                    level="ERROR",
                )
                return None

            summary = []
            for label, model_class in selected:
                created, skipped, conflicts = self._copy_records(
                    source_group,
                    target_group,
                    model_class,
                )
                summary.append(
                    f"{label}: created={created}, skipped={skipped}, conflicts={conflicts}"
                )

            self.message_user(
                request,
                (
                    f"Copied settings from '{source_group.name}' to "
                    f"'{target_group.name}'. " + " | ".join(summary)
                ),
            )
            return None

        source_group_choices = AccessGroup.objects.exclude(id=target_group.id)

        context = {
            **self.admin_site.each_context(request),
            "title": "Copy settings from another Access Group",
            "target_group": target_group,
            "source_group_choices": source_group_choices,
            "queryset": queryset,
            "action_name": "copy_from_access_group",
            "selected_ids": request.POST.getlist(ACTION_CHECKBOX_NAME),
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request,
            "admin/compass/accessgroup/copy_from_access_group.html",
            context,
        )

    copy_from_access_group.short_description = (
        "Copy settings from another Access Group"
    )


class AccessGroupContentAdminModel(SAMLAdminModel):
    list_display = ("name", "access_group", "editable")


class AccessGroupActiveContentAdminModel(AccessGroupContentAdminModel):
    list_display = ("name", "access_group", "active", "editable")


class ContactAdminModel(SAMLAdminModel):
    list_display = (
        "id",
        "student",
        "app_user",
        "contact_type",
        "contact_method",
        "access_groups_display",
        "checkin_date",
    )

    def access_groups_display(self, obj):
        return ", ".join(
            obj.access_group.order_by("name").values_list("name", flat=True)
        )

    access_groups_display.short_description = "Access groups"


admin_site = SAMLAdminSite(name='SAMLAdmin')
admin_site.register(AppUser, SAMLAdminModel)
admin_site.register(Student, SAMLAdminModel)
admin_site.register(AccessGroup, AccessGroupAdminModel)
admin_site.register(Affiliation, AccessGroupActiveContentAdminModel)
admin_site.register(EligibilityType, AccessGroupContentAdminModel)
admin_site.register(ContactType, AccessGroupActiveContentAdminModel)
admin_site.register(ContactMethod, AccessGroupActiveContentAdminModel)
admin_site.register(ContactTopic, AccessGroupActiveContentAdminModel)
admin_site.register(Contact, ContactAdminModel)
admin_site.register(OMADContactQueue, SAMLAdminModel)
admin_site.register(Visit, SAMLAdminModel)
admin_site.register(TokenProxy, SAMLAdminModel)
admin_site.register(Session, SessionAdminModel)
admin_site.register(StudentEligibility, SAMLAdminModel)
admin_site.register(VisitTutoringOption, SAMLAdminModel)
admin_site.register(VisitType, SAMLAdminModel)
