# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render

from ezi.views import ModelCrudApiView, ApiView

from Servers.common.auth_core.models import AuthUser

class AuthUserApiView(ModelCrudApiView):

    model = AuthUser

    allowed_methods = ("GET")
