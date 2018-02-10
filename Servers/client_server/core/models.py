# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import AbstractUser

class SecurityQuestion(models.Model):
    """
    A question that the system can ask in the event that the finger print
    scanner failed and the user forgot their username and password. If they
    answer one of these questions correctly, they will be granted access.
    """
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)


class Application(models.Model):
    """
    An abstract representation of an application that a user can log in to.
    """
    name = models.CharField(max_length=50)

    def json(self):
        return {
            "id": self.id,
            "pk": self.pk,
            "name": self.name
        }

    def create_session(self, user):
        """
        Creates an AuthenticatedSession object for this app and user. This
        assumes that the user has already been validated.
        """
        return self.authenticatedsession_set.create(user=user)

    def __str__(self):
        return self.name


class AuthUser(models.Model):
    """
    The basic user class that extends Django's base user class. This extension
    simply adds a copule things like security_questions and utility method.

    Fields:
        security_questions: The questions asked when a user forgot their
                            username and password.

        authenticated_apps: A list of apps that this user can log on to.
    """
    user = models.OneToOneField(User)
    security_questions = models.ManyToManyField(SecurityQuestion)
    authenticated_apps = models.ManyToManyField(Application, blank=True)

    def json(self):
        return {
            "id": self.id,
            "pk": self.pk,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.username,
            "password": self.user.password,
            "groups": [group.name for group in self.user.groups.all()],
            "security_questions": [q.question for q in self.security_questions.all()],
            "authenticated_apps": [app.json() for app in self.authenticated_apps.all()]
        }

    def __str__(self):
        return str(self.user)


class AuthenticatedSession(models.Model):
    """
    Represents a session where a user is logged in to a specific app. This is
    created after the user is successfuly validated by the fingerprint scanner
    or login page on the client server.

    Fields:
        app:        The Application object that this session is for.

        user:       The user that is logged into this sessions app through this
                    session.

        start:      The date and time that this session was started.
    """
    app = models.ForeignKey(Application)
    user = models.ForeignKey(AuthUser)
    start = models.DateTimeField(auto_now_add=True)
