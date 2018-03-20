# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from Servers.common.api_remotes.models import ClientServer

def register_client_server(modeladmin, request, queryset):
    for client_server in queryset:
        client_server.save_with_auth_server(request.user)

class ClientServerAdmin(admin.ModelAdmin):
    # fields = ["host", "username", "password"]
    actions = [register_client_server]

# Register your models here.
admin.site.register(ClientServer, ClientServerAdmin)
