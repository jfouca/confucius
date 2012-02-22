import os.path 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db',
    }
}

TIME_ZONE = None
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
PROJECT_DIR = os.path.dirname(__file__) 
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "confucius.context.get_current_path"

)

TEMPLATE_DIRS = (
   os.path.join(PROJECT_DIR, 'templates'),
) 
ROOT_URLCONF = 'confucius.urls'

INSTALLED_APPS = (
    'confucius',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

AUTHENTICATION_BACKENDS = ('confucius.backends.AccountBackend',)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/conference/home'
