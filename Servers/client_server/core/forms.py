from django import forms
from django.contrib.auth import authenticate, login

from Servers.common.auth_core.models import AuthUser
from core.models import NewUser
from core.pyfingerprint import PyFingerprint
class AuthenticationForm(forms.Form):
    """
    Form to log a user in to a client. This does not create the login session.
    It just validates the user. After they are validated by this, the user will
    have to be redirected to a page to select their app that they want to log in
    to. That page is where the AuthenticatedSession object will be created after
    they select their app.
    """
    user = None # Set in the clean method.
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean_username(self):
        """
        Cleans the username and makes sure that it is a valid username that
        matches an existing user.
        """
        username = self.cleaned_data.get("username", self.data["username"])
        if not username or not AuthUser.objects.filter_with_auth_server(user__username=username).exists():
            raise forms.ValidationError("No user with that username was found in our system.")
        return username

    def clean(self):
        """
        Override of the base classes clean method.

        Override: This override authenticates the username and password. If it
        is not valid, a ValidationError is thrown. If it is valid, then this
        classes user attribute is set to the user that is authenticated.
        """
        cleaned_data = super(AuthenticationForm, self).clean()
        username = cleaned_data.get("username", self.data["username"])
        password = cleaned_data.get("password", self.data["password"])
        user = AuthUser.objects.authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("The password and username entered did not match.")
        else:
            self.user = user
        return cleaned_data

    def save(self, request):
        """
        Override of the base classes save method.

        Override: Assuming the clean method has already been called, which sets
        this forms user to log in, this method will log that user in.
        """
        login(request, self.user)
        return self.user

class UserCreationForm(forms.ModelForm):
    """The creation of a new User"""
    class Meta:
        model=AuthUser
        fields=['password', 'fingerprint_image']

    username = forms.CharField(max_length=100)

    def save(self, *args, **kwargs):
        """
        Override of the base ModelForm save method. This saves the instance
        to be created by the input in the form.

        Override:
        Instead of just calling the save method, we need the django default
        User to be created first. This is done in the
        save_with_both_user_containers method so we want to call that.
        """
        auth_user = self.instance
        auth_user.save_with_both_user_containers(self.cleaned_data["username"])
        return auth_user
