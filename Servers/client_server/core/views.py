# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from core.forms import AuthenticationForm
from core.models import AuthenticatedSession

from ezi.views import ApiView

class LoginView(FormView):

    template_name = "core/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("core:app_choose")

    @method_decorator(sensitive_post_parameters("password"))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        This is an override of the base classes form_valid method. This gets
        called if the form is valid after a POST.

        If this is called, it is assumed that the form is valid. In this case,
        it is saved and then the super method is returned.

        Just because the form is valid, does not mean the username and password
        are correct (it just means the fields were individually valid)
        """
        self.user = form.save(self.request)
        print self.user
        return super(LoginView, self).form_valid(form)


class ApplicationChooserView(CreateView):

    model = AuthenticatedSession
    fields = ["app", "user"]
    success_url = reverse_lazy("core:login")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Override of dispatch to add login_required decorator"""
        return super(ApplicationChooserView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Sets the user as the initial argument to the hidden user field."""
        return {"user": self.request.user.id}
