from .settings_general import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3%aa)(81#=%4tn8c@=&u=1m@p%2%xhsnz+sbz+9r31%56q7)(m'

DEBUG = False

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'auth_server.wsgi.production.application'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
