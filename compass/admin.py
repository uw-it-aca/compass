# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import AppUser, Student, AccessGroup, Program, Contact, \
    ContactType, ContactTopic
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from uw_saml.utils import is_member_of_group


class SAMLAdminSite(admin.AdminSite):
    site_header = 'Compass admin'

    def __init__(self, *args, **kwargs):
        super(SAMLAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def has_permission(self, request):
        return is_member_of_group(request,
                                  settings.COMPASS_ADMIN_GROUP)

    def login(self, request, extra_context=None):
        if self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        else:
            return HttpResponseRedirect('/not-authorized/')


class AbstractSAMLAdminModel():
    def has_add_permission(self, request):
        return is_member_of_group(request,
                                  settings.COMPASS_ADMIN_GROUP)

    def has_change_permission(self, request, obj=None):
        return is_member_of_group(request,
                                  settings.COMPASS_ADMIN_GROUP)

    def has_delete_permission(self, request, obj=None):
        return is_member_of_group(request,
                                  settings.COMPASS_ADMIN_GROUP)

    def has_module_permission(self, request):
        return is_member_of_group(request,
                                  settings.COMPASS_ADMIN_GROUP)


class SAMLAdminModel(AbstractSAMLAdminModel, admin.ModelAdmin):
    pass


admin_site = SAMLAdminSite(name='SAMLAdmin')
admin_site.register(AppUser, SAMLAdminModel)
admin_site.register(Student, SAMLAdminModel)
admin_site.register(AccessGroup, SAMLAdminModel)
admin_site.register(Program, SAMLAdminModel)
admin_site.register(ContactType, SAMLAdminModel)
admin_site.register(ContactTopic, SAMLAdminModel)
admin_site.register(Contact, SAMLAdminModel)
