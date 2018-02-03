from .settings_general import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v1z!!79ja%a^hd&9i6eouu-tkhy%+s)lgs4$)cr9=3ov@e+@i('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WSGI_APPLICATION = 'client_server.wsgi.development.application'
