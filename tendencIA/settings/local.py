from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.sqlite3',
 'NAME':
os.path.join(os.path.dirname(BASE_DIR),'db_local.db'),
 }
}