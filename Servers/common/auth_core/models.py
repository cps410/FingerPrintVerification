# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import requests

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models

from django.contrib.auth.models import AbstractUser

from ezi.utils import RestApiGetParameter

from Servers.common.api_remotes.auth_server import AuthApiConnection
from Servers.common.utils import SERVER_TYPE_CLIENT, SERVER_TYPE_CENTRAL

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
            "user": self.user.pk,
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

    def create_or_update_from_json(self, json):
        if not json: return None
        username = json["username"]
        try:
            auth_user = self.get(user__username=username)
            auth_user.update_from_json(json)
            return auth_user
        except AuthUser.DoesNotExist:
            return self.create_from_json(json)

    def create_from_json(self, json):
        """
        Creates a single AuthUser object from the given json. This json is
        expected to be a single json object representing an AuthUser. The format
        of this json is expected to be that generated in AuthUser.json()

        If nothing is supplied in json, None will be returned.
        """
        if not json: return None
        user = User.objects.create(username=json["username"], first_name=json["first_name"],
                                    last_name=json["last_name"], email=json["email"])
        user.set_password(json["password"])
        user.save()
        auth_user = AuthUser.objects.create(user=user, password=json["password"])
        for app_json in json["authenticated_apps"]:
            app = Application.objects.get(name=app_json["name"])
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
            remote_records = self._read_users_from_auth_response(AuthApiConnection.get_users(**kwargs))
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
            records = self._read_users_from_auth_response(AuthApiConnection.get_users(**kwargs))
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
    fingerprint_image = models.ImageField(upload_to='Images/')

    def update_from_json(self, json):
        """
        Takes the data from json and updates this auth_user and its related
        objects according to what's in json. The format of json is expected to
        be identical to AuthUser.json().
        """
        user = self.user

        user.first_name=json["first_name"]
        user.last_name=json["last_name"]
        user.email=json["email"]
        user.username=json["username"]
        user.save()

        user.groups.set(Group.objects.filter(name__in=json["groups"]))

        self.password=json["password"]
        self.save()

        self.authenticated_apps.set(Application.objects.filter(name__in=[app["name"] for app in json["authenticated_apps"]]))

        self.securityquestion_set.all().delete()
        for question_json in json["security_questions"]:
            SecurityQuestion.objects.create(**question_json)
        return self


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

    def _save_with_auth_server(self):
        if settings.SERVER_TYPE == SERVER_TYPE_CENTRAL:
            # If this is on the central server, we are already saving "with the
            # auth server" so this method is unneeded. It would also result in
            # a recursion issue because the auth server would start making calls
            # to itself then.
            return None

        try:
            created_user_json = AuthApiConnection.save_user(self)
            return created_user_json["id"]
        except AuthApiConnection.ResponseError:
            # Wait for later to save the user to the master database. Maybe the
            # server will work then.
            #
            # TODO: Save the fact that this still needs to be saved.
            return

    def save_with_both_user_containers(self, username, *args, **kwargs):
        """
        Creates the django.contrib.auth.models.User object before saving this
        AuthUser so that the relationship can be set. Then the AuthUser will be
        saved with a relationship to the created django User.
        """
        user = User.objects.create_user(username, "", self.password)
        self.user = user
        self.save()

    def save(self, *args, **kwargs):
        """Syncs the override password with this password."""
        self.user.set_password(self.password)
        auth_user = super(AuthUser, self).save(*args, **kwargs)
        auth_server_assigned_id = self._save_with_auth_server()
        return auth_user

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
