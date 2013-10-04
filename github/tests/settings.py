import os

SITE_ID = 1

APP_ROOT = os.path.abspath(os.path.dirname(__file__))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

AUTHENTICATION_BACKENDS = (
    'github.backends.GithubBackend',
)

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


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'github.middlewares.GithubAuthorizationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SECRET_KEY = 'foobar'

TEST_RUNNER = 'discover_runner.DiscoverRunner'

TEMPLATE_DIRS = (os.path.join(APP_ROOT, 'templates'),)

ROOT_URLCONF = 'github.tests.urls'

AUTH_USER_MODEL = os.environ.get('AUTH_USER_MODEL', 'auth.User')
