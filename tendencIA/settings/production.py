from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','production-domain.com']


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.mysql',
 'NAME':os.getenv('DB_NAME'),
 'USER':os.getenv('DB_USER')
 'PASSWORD': os.getenv('DB_PASSWORD'),
 'HOST': os.getenv('DB_HOST'),
 'PORT': os.getenv('DB_PORT'),
 }
}

os.environ['DJANGO_PORT'] = '8080'