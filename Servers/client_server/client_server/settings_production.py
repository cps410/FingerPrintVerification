from .settings_general import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v1z!!79ja%a^hd&9i6eouu-tkhy%+s)lgs4$)cr9=3ov@e+@i('

DEBUG = False

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'client_server.wsgi.production.application'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
