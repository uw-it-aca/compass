# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import Group
from compass.models import User, Student, AccessGroup, Program, Contact, \
    ContactType, ContactTopic


class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s, *a ,**kw: True


admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True

admin.site.unregister(AuthUser)
admin.site.unregister(Group)

admin.site.register(User)
admin.site.register(Student)
admin.site.register(AccessGroup)
admin.site.register(Program)
admin.site.register(ContactType)
admin.site.register(ContactTopic)
admin.site.register(Contact, SimpleHistoryAdmin)
