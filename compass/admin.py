# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import (
    AppUser, Student, AccessGroup, Affiliation, Contact,
    ContactType, ContactMethod, ContactTopic, EligibilityType)
from compass.dao.group import is_admin_user
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rest_framework.authtoken.models import Token, TokenProxy


class SAMLAdminSite(admin.AdminSite):
    site_header = 'Compass admin'

    def __init__(self, *args, **kwargs):
        super(SAMLAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def has_permission(self, request):
        return is_admin_user(request)

    def login(self, request, extra_context=None):
        if self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        else:
            return HttpResponseRedirect('/not-authorized/')


class AbstractSAMLAdminModel():
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
    list_display = ['user', 'session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']


admin_site = SAMLAdminSite(name='SAMLAdmin')
admin_site.register(AppUser, SAMLAdminModel)
admin_site.register(Student, SAMLAdminModel)
admin_site.register(AccessGroup, SAMLAdminModel)
admin_site.register(Affiliation, SAMLAdminModel)
admin_site.register(EligibilityType, SAMLAdminModel)
admin_site.register(ContactType, SAMLAdminModel)
admin_site.register(ContactMethod, SAMLAdminModel)
admin_site.register(ContactTopic, SAMLAdminModel)
admin_site.register(Contact, SAMLAdminModel)
admin_site.register(TokenProxy, SAMLAdminModel)
admin_site.register(Session, SessionAdminModel)
