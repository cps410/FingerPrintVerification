# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser

class SecurityQuestion(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

class AuthUser(AbstractUser):
    security_questions = models.ManyToManyField(SecurityQuestion)

    def json(self):
        return {
            "id": self.id,
            "pk": self.pk,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "groups": [group.name for group in self.groups.all()],
            "security_questions": [q.question for q in self.security_questions.all()]
        }
