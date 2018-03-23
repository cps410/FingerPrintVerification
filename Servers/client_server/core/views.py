#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import serial

from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from core.forms import AuthenticationForm, UserCreationForm, LocalSuperAuthUserCreationForm
from Servers.common.auth_core.models import AuthenticatedSession
from core.pyfingerprint import PyFingerprint


from ezi.views import ApiView

@method_decorator(login_required, name="dispatch")
class LoginView(FormView):

    template_name = "auth_core/login.html"
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


@login_required
def logout_view(request):
    """
    Logs the currently logged in user out of the session and redirects them to
    the login page.

    If the user already isn't logged in, the login_required decorator will just
    kick them to the login page automatically.
    """
    logout(request)
    return HttpResponseRedirect(reverse("core:login"))


class ApplicationChooserView(CreateView):

    model = AuthenticatedSession
    fields = ["app", "user"]
    success_url = reverse_lazy("core:logout")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Override of dispatch to add login_required decorator"""
        return super(ApplicationChooserView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Sets the user as the initial argument to the hidden user field."""
        return {"user": self.request.user.id}

def fingerprint_scan(request):
# initialize sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    except Exception as e:
        print('The fingerprint sensor failed.')
        print('Exception message: ' + str(e))

    ## Tries to read image and download it
    try:
        print('Waiting for finger...')
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        print('Downloading image (this may take a while)...')
        imageDestination = 'Images/fingerprint.bmp'
        f.downloadImage(imageDestination)
        print('The image was saved to "' + imageDestination + '".')
    except Exception as e:
        print('Exception message: ' + str(e))
        return HttpResponse("did not work")
    return HttpResponse("worked, image is now available in the temp folder /Images/")

class NewUserView(FormView):
    """New User Creation"""
    form_class = UserCreationForm
    template_name = "auth_core/newuser.html"
    success_url = reverse_lazy("core:login")

    def form_valid(self, form):
        """
        This is an override of the base classes form_valid method. This gets
        called if the form is valid after a POST.

        If this is called, it is assumed that the form is valid. In this case,
        it is saved and then the super method is returned.

        Just because the form is valid, does not mean the username and password
        are correct (it just means the fields were individually valid)
        """
        self.newuser = form.save()
        print self.newuser
        return super(NewUserView, self).form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy("admin:login")), name="dispatch")
class CreateLocalAuthUser(FormView):
    """
    Form to create a local auth user for a super user without saving it to the
    central server.
    """
    form_class = LocalSuperAuthUserCreationForm
    template_name = "auth_core/create_local_auth_user.html"
    success_url = "admin:auth_core_authuser_change"

    def dispatch(self, request, *args, **kwargs):
        """
        Override of base FormView dispatch to ensure that the logged in user
        is a staff member and a superuser. If not, they are redirected to the
        login page.
        """
        if not (request.user.is_staff and request.user.is_superuser):
            return HttpResponseRedirect(reverse("admin:login"))
        return super(CreateLocalAuthUser, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        This is an override of the base classes form_valid method. This gets
        called if the form is valid after a POST.

        If this is called, it is assumed that the form is valid. In this case,
        it is saved and then the super method is returned.

        Override:
        This adds the primary key to the success_url as an argument to the
        reverse_lazy call.
        """
        auth_user = form.save()
        return HttpResponseRedirect(reverse(self.success_url, args=[auth_user.pk]))
