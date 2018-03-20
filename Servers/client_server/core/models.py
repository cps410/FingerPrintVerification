# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class NewUser(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    fingerprint_image=models.ImageField(upload_to='Images/')
