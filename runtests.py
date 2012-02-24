#!/usr/bin/env python

from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        },
    },
    INSTALLED_APPS=(
        'confucius',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    ),
    ROOT_URLCONF='confucius.urls',
)

if __name__ == '__main__':
    import sys
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=0)
    failures = runner.run_tests(None)
    sys.exit(failures)
