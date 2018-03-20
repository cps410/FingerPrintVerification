# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from Servers.common.api_remotes.auth_server import AuthApiConnection
from Servers.common.utils import SERVER_TYPE_CLIENT, SERVER_TYPE_CENTRAL

class ClientServerAuthenticationMissingError(Exception):
    def __init__(self, message, *args, **kwargs):
        if not message: message = "The authentication object (django.contrib.auth.models.User) could not be found for this Client Server."
        super(ClientServerAuthenticationMissingError, self).__init__(message, *args, **kwargs)

# class ClientServerManager(models.Manger):
#
#     def register_client(self, host, username, password):
#         client_server = self.create(host=host, username=username, password)

class ClientServer(models.Model):
    """
    Contains the authentication for a client servers account on the auth server.

    This object also has an auth.User object attached to it using username as a
    sort of ForeignKey for the relationship but because the client server does
    not connect a user with this object. So on the auth server, it has a user,
    but on the client server, it does not. Therefore the schema does not for
    certain have a ForeignKey to the user. Rather than use if statements and
    logic to decide if the field should be added, the user will be a soft
    ForeignKey where the key is the username.

    To access the user object for this ClientServer object, use the property
    named 'user' as the accessor.
    """

    host = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    @property
    def user(self):
        """
        Returns the user that represents the authentication for this client
        server. This method doesn't use this ClientServer object to get the
        user, it uses the last saved record of this ClientServer object with
        the same id. This is because, if the username was changed, then the
        user to update can't be find because the query would be using the new
        username that hasn't been saved with the user yet.

        If the user was not found, there are two things that could happen.

        1. This ClientServer object is just being created and so doesn't have
            a user.
        2. If this ClientServer object already exists (self.pk is not None),
            then something went wrong if there is no User object with it's
            username. Error is thrown in this case.
        """
        if self.pk: last_saved_self = ClientServer.objects.get(pk=self.pk)
        else: last_saved_self = self

        try:
            authentication = User.objects.get(username=last_saved_self.username)
            return authentication
        except User.DoesNotExist as e:
            if not self.pk:
                # Create user since this ClientServer object is just being
                # created.
                authentication = User.objects.create_user(self.username, "", self.password)
                authentication.is_staff = True
                authentication.is_superuser = True
                authentication.save()
                return authentication
            else:
                # This ClientServer object already exists and therefore must
                # have a user obejct for it's username. If this line is
                # reached, we know there is no user so something went wrong.
                raise ClientServerAuthenticationMissingError("No user found ")

    def _update_user(self):
        """
        Updates the user that represents the authentication for this client
        server.
        """
        authentication = self.user
        # If user was created in self.user call, it will still be updated in the
        # next couple lines. There's no change but still a write so we'll just
        # let it happen.
        authentication.username = self.username
        authentication.set_password(self.password)
        authentication.save()
        return authentication

    def save_with_auth_server(self, superuser):
        """
        Initiates call to the auth server to save this ClientServer object.
        """
        if settings.SERVER_TYPE == SERVER_TYPE_CENTRAL: return
        registered_client_json = AuthApiConnection.register_client_with_auth(self, superuser)
        return bool(registered_client_json)

    def json(self):
        return {
            "username": self.username,
            "password": self.password,
            "host": self.host,
        }

    def save(self, *args, **kwargs):
        """
        Override of base save method in order to update the User object attached
        to this ClientServer object if this is the central server or call the
        auth server to save this object if this is a client server.
        """
        if settings.SERVER_TYPE == SERVER_TYPE_CENTRAL:
            # Save the actual user object.
            self._update_user()
        super(ClientServer, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.host)
