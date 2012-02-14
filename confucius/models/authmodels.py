from django.contrib.auth.models import User as AuthUser
from django.db import models


class User(AuthUser):
    class Meta:
        app_label = "confucius"
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

        if len(errors):
            raise ValidationError(errors)

    def validate_unique(self, exclude=None):
        super(User, self).validate_unique(exclude)
        from django.core.exceptions import ValidationError

        try:
            User.objects.get(email__iexact=self.email)
            raise ValidationError(
                    {'email': [u'User with this Email already exists.']})
        except User.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.full_clean()
        super(User, self).save(*args, **kwargs)


class Language(models.Model):
    class Meta:
        app_label = "confucius"

    code = models.CharField(max_length=2)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    class Meta:
        app_label = "confucius"

    user = models.OneToOneField(User)
    secondary_email = models.EmailField(blank=True)
    primary_postal_address = models.TextField()
    secondary_postal_address = models.TextField(blank=True)
    languages = models.ManyToManyField(Language)

