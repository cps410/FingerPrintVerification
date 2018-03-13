# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import AbstractUser

from ezi.utils import RestApiGetParameter

from Servers.common.api_remotes.auth_server import AuthApiConnection

class SecurityQuestion(models.Model):
    """
    A question that the system can ask in the event that the finger print
    scanner failed and the user forgot their username and password. If they
    answer one of these questions correctly, they will be granted access.
    """

    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    user = models.ForeignKey("AuthUser")

    def json(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "auth_user": self.user.pk,
        }


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


class AuthUserManager(models.Manager):

    def _query_auth_server(self, **kwargs):
        """
        Makes a call to the centralized auth server for users with the given
        kwargs. This returns the users returned as json data.
        """
        # Build url for users
        rest_api_get_params = [RestApiGetParameter(2, param_name, param_value) for
                                param_name, param_value in kwargs.items()]
        request_url = "/core/api/user/"
        request_url = request_url + "?" + "&".join([ "=".join(param.format()) for param in rest_api_get_params ])

        api_connection = AuthApiConnection(settings.AUTH_SERVER_HOST,
                            settings.AUTH_SERVER_CREDENTIALS["username"],
                            settings.AUTH_SERVER_CREDENTIALS["password"])
        api_connection.login()

        user_response = api_connection.get(request_url)

        if user_response.status_code == 200:
            users_json_text =  user_response.text
            return json.loads(users_json_text)["response"]
        else:
            raise ValueError("Could not retrieve users from central server. Status Code: {}".format(user_response.status_code))

    def _read_users_from_auth_response(self, users_json):
        """
        Parses a Json object that represents a user into an AuthUser object.
        Returns all users created. user_json should be a list of AuthUser
        in json format (using AuthUser.json format).
        """
        users = self.none()
        for user_json in users_json:
            users = users | AuthUser.objects.filter(id=self.create_from_json(user_json).id)
        return users

    def create_from_json(self, json):
        """
        Creates a single AuthUser object from the given json. This json is
        expected to be a single json object representing an AuthUser.
        """
        user = User.objects.create(username=json["username"], password=json["password"],
                                    first_name=json["first_name"], last_name=json["last_name"],
                                    email=json["email"])
        auth_user = AuthUser.objects.create(user=user, password=json["password"])
        for app_json in json["authenticated_apps"]:
            app, app_was_created = Application.objects.get_or_create(name=app_json["name"])
            auth_user.authenticated_apps.add(app)

        for question_json in json["security_questions"]:
            question = SecurityQuestion.objects.create(question=question_json["question"],
                                answer=question_json["answer"], user=auth_user)

        return auth_user

    def get_with_auth_server(self, **kwargs):
        """
        Returns a single AuthUser from the local database or the master central
        server. If one doesn't exist locally, the central database will be
        queried to see if it exists on that server. If so, those users will
        be returned.

        The AuthUser returned will match the kwargs given.
        """
        try:
            local_record = self.get(**kwargs)
            return local_record
        except AuthUser.DoesNotExist:
            remote_records = self._read_users_from_auth_response(self._query_auth_server(**kwargs))
            if remote_records.count() > 1:
                raise AuthUser.MultipleObjectsReturned("Multiple AuthUsers were found.")
            elif remote_records.count() < 1:
                raise AuthUser.DoesNotExist("No AuthUser was found.")
            return remote_records[0]

    def filter_with_auth_server(self, **kwargs):
        """
        Returns list of AuthUsers from the local database or the master central
        server. If no AuthUser exists locally, the central database will be
        queried to see if any exists on that server. If so, those users will
        be returned.

        The AuthUsers returned will match the kwargs given.
        """
        records = self.filter(**kwargs)
        if not records:
            records = self._read_users_from_auth_response(self._query_auth_server(**kwargs))
        return records

    def authenticate(self, username, password):
        """A cheap authentication function."""
        try:
            auth_user = self.get_with_auth_server(user__username=username, password=password)
            return auth_user.user
        except (AuthUser.DoesNotExist, ValueError):
            return self.none()


class AuthUser(models.Model):
    """
    The basic user class that extends Django's base user class. This extension
    simply adds a copule things like security_questions and utility method.

    Fields:
        password:           An override field for the users password. We are not
                            using self.user.password in order to avoid the
                            encryption.
        security_questions: The questions asked when a user forgot their
                            username and password.

        authenticated_apps: A list of apps that this user can log on to.
    """
    objects = AuthUserManager()

    user = models.OneToOneField(User)
    password = models.CharField(max_length=15)
    authenticated_apps = models.ManyToManyField("Application", blank=True)

    def json(self):
        return {
            "id": self.id,
            "pk": self.pk,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "username": self.user.username,
            "password": self.password,
            "groups": [group.name for group in self.user.groups.all()],
            "security_questions": [q.json() for q in self.securityquestion_set.all()],
            "authenticated_apps": [app.json() for app in self.authenticated_apps.all()]
        }

    def save(self, *args, **kwargs):
        """Syncs the override password with this password."""
        self.user.set_password(self.password)
        return super(AuthUser, self).save(*args, **kwargs)

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

    app = models.ForeignKey("Application")
    user = models.ForeignKey("AuthUser")
    start = models.DateTimeField(auto_now_add=True)
