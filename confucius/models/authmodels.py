from django.contrib.auth.models import User as AuthUser
from django.db import models


class User(AuthUser):
    class Meta:
        proxy = True

    def clean(self):
        super(User, self).clean()

        from django.core.exceptions import ValidationError
        from django.core.validators import EMPTY_VALUES

        errors = {}

        if self.last_name in EMPTY_VALUES:
            errors['last_name'] = [u'This field cannot be blank.']
        if self.email in EMPTY_VALUES:
            errors['email'] = [u'This field cannot be blank.']
        try:
            User.objects.get(email__iexact=self.email)
            errors['email'] = [u'User with this Email already exists.']
        except User.DoesNotExist:
            pass

        if len(errors):
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)


class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User)
    secondary_email = models.EmailField(blank=True)
    primary_postal_address = models.TextField()
    secondary_postal_address = models.TextField(blank=True)
    languages = models.ManyToManyField(Language)
