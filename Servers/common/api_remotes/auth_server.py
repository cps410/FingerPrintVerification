import json
import requests

from django.conf import settings

class AuthApiConnection:

    class ResponseError(Exception):
        def __init__(self, message):
            super(AuthApiConnection.ResponseError, self).__init__(message)

    class URLS:
        LOGIN = "/helm/login/?next=/helm/"
        USER_ACCESS = "/core/api/user/"
        CSRF_ACCESS = "/core/api/csrf_token/"

    host = None
    username = None
    password = None
    session = None
    cookies = None

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    @property
    def csrf_token(self):
        url = "{}{}".format(self.host, AuthApiConnection.URLS.CSRF_ACCESS)
        csrf_response = self.session.get(url)
        if not csrf_response.status_code == 200:
            raise AuthApiConnection.ResponseError("Could not get csrf_token. Status Code was {}.".format(csrf_response.status_code))
        self.cookies = csrf_response.cookies
        return self.session.cookies.get("csrftoken", "")

    def header(self, csrftoken):
        return {
            "X-CSRFToken": csrftoken,
            "Referer": "{}{}".format(self.host, self.URLS.CSRF_ACCESS)
        }

    def login(self):
        """
        Logs the session on to the auth server using this objects username and
        password.

        We can't use the csrf_token getter cause the url it uses requires a
        login.
        """
        self.session = requests.Session()
        url = "{}{}".format(self.host, AuthApiConnection.URLS.LOGIN)
        self.session.get(url)
        csrf_token = self.session.cookies.get("csrftoken", "")
        login_post = self.session.post(url, {
            "username": self.username,
            "password": self.password,
            "csrfmiddlewaretoken": csrf_token
        })
        if not login_post.status_code == 200:
            raise AuthApiConnection.ResponseError("Could not log in to auth server. Status Code was {}.".format(login_post.status_code))
        if "Please enter the correct username and password for a staff account." in login_post.text:
            raise AuthApiConnection.ResponseError("Login credentials were incorrect.")
        self.cookies = self.session.cookies

    def data_with_csrf(self, data):
        data["csrfmiddlewaretoken"] = self.csrf_token
        return data

    def get(self, url):
        full_url = "{}{}".format(self.host, url)
        response = self.session.get(full_url, cookies=self.cookies)
        return response

    def post(self, url, POST={}):
        full_url = "{}{}".format(self.host, url)
        data = self.data_with_csrf(POST)
        response = self.session.post(full_url, data, cookies=self.cookies, headers=self.header(data["csrfmiddlewaretoken"]))
        return response

    def put(self, url, PUT={}):
        full_url = "{}{}".format(self.host, url)
        data = self.data_with_csrf(PUT)
        response = self.session.put(full_url, data, cookies=self.cookies, headers=self.header(data["csrfmiddlewaretoken"]))
        return response

    @classmethod
    def save_user(cls, user):
        api_connection = cls(settings.AUTH_SERVER_HOST,
                            settings.AUTH_SERVER_CREDENTIALS["username"],
                            settings.AUTH_SERVER_CREDENTIALS["password"])
        api_connection.login()

        put_data = {"auth_user": json.dumps(user.json())}
        user_save_response = api_connection.put(cls.URLS.USER_ACCESS, put_data)
        del(api_connection)

        if user_save_response.status_code == 200:
            user_save_json_text = user_save_response.text
            return json.loads(user_save_json_text)["response"]
        else:
            raise AuthApiConnection.ResponseError("Could not save user to master server. Status Code: {}".format(user_save_response.status_code))

    @classmethod
    def get_users(cls, **kwargs):
        """
        Makes a call to the centralized auth server for users with the given
        kwargs. This returns the users returned as json data.
        """
        # Build url for users
        rest_api_get_params = [RestApiGetParameter(2, param_name, param_value) for
                                param_name, param_value in kwargs.items()]
        request_url = cls.URLS.USER_ACCESS + "?" + "&".join([ "=".join(param.format()) for param in rest_api_get_params ])

        api_connection = cls(settings.AUTH_SERVER_HOST,
                            settings.AUTH_SERVER_CREDENTIALS["username"],
                            settings.AUTH_SERVER_CREDENTIALS["password"])
        api_connection.login()

        user_response = api_connection.get(request_url)
        del(api_connection)

        if user_response.status_code == 200:
            users_json_text =  user_response.text
            return json.loads(users_json_text)["response"]
        else:
            raise AuthApiConnection.ResponseError("Could not retrieve users from central server. Status Code: {}".format(user_response.status_code))
