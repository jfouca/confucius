from django.contrib.auth.models import User
from django.db import models


class ConfuciusUser(User):
    class Meta:
        proxy = True

    def clean(self):
        from django.core import exceptions, validators
        for field in [self.last_name, self.email]:
            if(field in validators.EMPTY_VALUES):
                raise exceptions.ValidationError(
                    models.Field.default_error_messages['blank'])
        super(ConfuciusUser, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ConfuciusUser, self).save(*args, **kwargs)


class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(ConfuciusUser)
    secondary_email = models.EmailField(blank=True)
    primary_postal_address = models.TextField()
    secondary_postal_address = models.TextField(blank=True)
    languages = models.ManyToManyField(Language)
