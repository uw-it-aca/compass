# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import Group, User
from compass.models import AppUser, Student, AccessGroup, \
    Program, Contact, ContactType, ContactTopic


class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s, *a, **kw: True


admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(AppUser)
admin.site.register(Student)
admin.site.register(AccessGroup)
admin.site.register(Program)
admin.site.register(ContactType)
admin.site.register(ContactTopic)
admin.site.register(Contact, SimpleHistoryAdmin)
