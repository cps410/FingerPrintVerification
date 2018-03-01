from .settings_general import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3%aa)(81#=%4tn8c@=&u=1m@p%2%xhsnz+sbz+9r31%56q7)(m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["141.209.48.202", "localhost"]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WSGI_APPLICATION = 'auth_server.wsgi.development.application'
