from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete

from confucius.utils import email_to_username


class AccountManager(models.Manager):
    def create(self, email, password, last_name, is_active=False):
        email = email.lower()
        username = email_to_username(email)
        now = datetime.now()

        user = User(username=username, is_staff=False, is_active=is_active,
            is_superuser=False, last_login=now, date_joined=now)
        user.set_password(password)
        user.save(using=self._db)

        account = Account(user=user)
        account.save(using=self._db)

        email_address = EmailAddress(account=account, main=True, value=email)
        email_address.save(using=self._db)

        return account


class Account(models.Model):
    user = models.OneToOneField(User)
    languages = models.ManyToManyField('Language', blank=True)

    objects = AccountManager()

    class Meta:
        app_label = 'confucius'

    def __getattr__(self, name):
        if name in ('username', 'first_name', 'last_name', 'is_active',
                'check_password', 'set_password'):
            return getattr(self.user, name)
        return super(Account, self).__getattr__(name)

    def __unicode__(self):
        return unicode(self.emailaddress_set.all()[0])

    def add_email(self, email):
        email_address = EmailAddress(account=self, value=email)
        email_address.save()


class Address(models.Model):
    account = models.ForeignKey(Account)
    main = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'confucius'

    def __unicode__(self):
        return self.value


class EmailAddress(Address):
    value = models.EmailField(unique=True)


class PostalAddress(Address):
    name = models.CharField(max_length=31)
    value = models.TextField()


class Language(models.Model):
    code = models.CharField(max_length=5, choices=settings.LANGUAGES)

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.code


def delete_user(sender, instance, **kwargs):
    User.objects.get(pk=instance.user_id).delete()

post_delete.connect(delete_user, sender=Account)
