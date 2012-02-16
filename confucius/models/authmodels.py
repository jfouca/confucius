from django.contrib.auth.models import User
from django.db import models

from confucius.utils import email_to_username


class AccountQuerySet(models.query.QuerySet):
    def delete(self):
        for instance in self:
            User.objects.get(pk=instance.user_id).delete()


class AccountManager(models.Manager):
    def create(self, email, password, last_name, is_active=False):
        from datetime import datetime

        email = email.lower()
        username = email_to_username(email)
        now = datetime.now()

        user = User(username=username, last_name=last_name, is_staff=False,
            is_active=is_active, is_superuser=False, last_login=now,
            date_joined=now)
        user.set_password(password)
        user.save(using=self._db)

        account = Account(user=user)
        account.save(using=self._db)

        email_address = EmailAddress(account=account, main=True, value=email)
        email_address.save(using=self._db)

        return account

    def get_query_set(self):
        return AccountQuerySet(model=self.model, using=self._db)

    def get_by_email(self, email):
        return self.get(emailaddress__value__exact=email)


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

    def __setattr__(self, name, value):
        if name in ('username', 'first_name', 'last_name', 'is_active',
                'check_password', 'set_password'):
            return setattr(self.user, name, value)
        return super(Account, self).__setattr__(name, value)

    def __getitem__(self, index):
        if index in ('username', 'first_name', 'last_name', 'is_active',
                'check_password', 'set_password'):
            return self.user[index]

    def __unicode__(self):
        return unicode(self.user.first_name+" "+self.user.last_name+" <"+unicode(self.get_main_emailaddress())+">")

    def add_email(self, email):
        email_address = EmailAddress(account=self, value=email)
        email_address.save()

    def get_main_emailaddress(self):
        return self.emailaddress_set.get(main=True)

    def has_email(self, email):
        try:
            self.emailaddress_set.get(value=email)
            return True
        except EmailAddress.DoesNotExist:
            return False

    def save(self, *args, **kwargs):
        self.user.save()
        super(Account, self).save(*args, **kwargs)

    def delete(self):
        Account.objects.filter(pk=self.pk).delete()


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
    code = models.CharField(max_length=5)
    value = models.CharField(max_length=25)

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.value
