from django.contrib.auth.models import User
from django.db import models
from confucius.utils import email_to_username


class AccountQuerySet(models.query.QuerySet):
    def delete(self):
        """
        We want to delete the User because it will apply the CASCADE strategy
        to all entities linked to it : basically every model in this file.

        It is necessary to override the delete() method of the default QuerySet
        as it never calls the delete() method of the model when deleting a
        set of entities (returned by filter() or all() for instance).
        """
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

    def __unicode__(self):
        return unicode(self.user.first_name+" "+self.user.last_name+" <"+unicode(self.get_main_email())+">")

    def add_email(self, email):
        email_address = EmailAddress(account=self, value=email)
        email_address.save()

    def get_main_email(self):
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
        """
        We want to delete the User because it will apply the CASCADE strategy
        to all entities linked to it : basically every model in this file.
        """
        User.objects.get(pk=self.user_id).delete()


class Address(models.Model):
    account = models.ForeignKey(Account)
    main = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'confucius'

    def __unicode__(self):
        return self.value

    def validate_unique(self, exclude=None):
        from django.core.exceptions import ValidationError

        # Check that each Account has only one main Address
        main_address = Account.objects.get(pk=self.account_id)
        """
        raise Exception(dict(self))
        if self is not main_address and self.main:
            raise ValidationError({'value': [u'There can only be one main '
                + self._meta.get_field('value').verbose_name]})
        """


class EmailAddress(Address):
    value = models.EmailField(unique=True, verbose_name="email")


class PostalAddress(Address):
    value = models.TextField(verbose_name="address")


class Language(models.Model):
    code = models.CharField(max_length=5)
    value = models.CharField(max_length=25)

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.value
