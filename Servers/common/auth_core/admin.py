# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from Servers.common.auth_core.models import AuthUser, SecurityQuestion, Application, AuthenticatedSession

# Register your models here.
admin.site.register([AuthUser, SecurityQuestion, Application, AuthenticatedSession])
