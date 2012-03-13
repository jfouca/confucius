from django.db.models import signals

from confucius import models as confucius_app
from confucius.models import Email, User
from confucius.utils import email_to_username


def modify_superuser(app, created_models, verbosity, **kwargs):
    if confucius_app.Email in created_models and User.objects.filter(pk=1).exists():
        user = User.objects.get(pk=1)
        user.username = email_to_username(user.email)
        user.save()
        Email.objects.create(value=user.email, user=user, main=True, confirmed=True)


signals.post_syncdb.connect(modify_superuser, sender=confucius_app, dispatch_uid='confucius.management.modify_superuser')
