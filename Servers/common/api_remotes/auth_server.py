import requests

class AuthApiConnection:

    class URLS:
        LOGIN = "/helm/login/?next=/helm/"
        USER_ACCESS = "/api/core/user/"

    host = None
    username = None
    password = None
    session = None
    csrf_token = None

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def login(self):
        """
        Logs the session on to the auth server using this objects username and
        password.
        """
        self.session = requests.Session()
        url = "{}{}".format(self.host, AuthApiConnection.URLS.LOGIN)
        self.session.get(url)
        self.csrf_token = self.session.cookies.get("csrftoken", "")
        login_post = self.session.post(url, {
            "username": self.username,
            "password": self.password,
            "csrfmiddlewaretoken": self.csrf_token
        })
        if not login_post.status_code == 200:
            raise ValueError("Could not log in to auth server. status was {}.".format(login_post.status_code))

    def get(self, url):
        host_url = "{}{}".format(self.host, url)
        return self.session.get(host_url)

    def post(self, url, POST={}):
        host_url = "{}{}".format(self.host, url)
        return self.session.post(url, host_url)
