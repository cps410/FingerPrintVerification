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
import time

from core.forms import AuthenticationForm, UserCreationForm, LocalSuperAuthUserCreationForm
from Servers.common.auth_core.models import AuthenticatedSession
from core.pyfingerprint import PyFingerprint


from ezi.views import ApiView

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
        f.convertImage(0x01)
        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
        auth_user = request.user.authuser
        auth_user.positionNumber = positionNumber
        auth_user.save()
        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')
        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()

        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        print('The image was saved to "' + imageDestination + '".')


    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        print('Exception message: ' + str(e))
        return HttpResponse("did not work")
        exit(1)

    return HttpResponse("worked, image is now available in the temp folder /Images/")

def fingerprint_enrollment(request):
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    """
    PyFingerprint
    Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
    All rights reserved.

    THIS CODE HAS BEEN ALTERED FROM ITS ORIGINAL FORM

    """


    ## Enrolls new finger
    ##

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

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
