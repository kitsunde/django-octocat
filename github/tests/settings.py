import os

SITE_ID = 1

APP_ROOT = os.path.abspath(os.path.dirname(__file__))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'github',
]

SECRET_KEY = 'foobar'

TEST_RUNNER = 'discover_runner.DiscoverRunner'

TEMPLATE_DIRS = (os.path.join(APP_ROOT, 'templates'),)

ROOT_URLCONF = 'github.tests.urls'