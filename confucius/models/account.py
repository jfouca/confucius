from django.contrib.auth.models import User
from django.db import models


class BaseConfucius(models.Model):
    """
    Base class for models which belong to confucius.
    Used mainly to avoid adding a Meta class with the
    right app_label for each model.
    """
    class Meta:
        abstract = True
        app_label = 'confucius'


class Email(BaseConfucius):
    user = models.ForeignKey(User, related_name='emails')
    main = models.BooleanField(default=False)
    value = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        """
        When saved, if self is a main address it should update the User's email
        with its value.
        """
        from confucius.utils import email_to_username

        super(Email, self).save(*args, **kwargs)

        if self.main:
            self.user.email = self.value
            self.user.username = email_to_username(self.value)
            self.user.save()

    def __unicode__(self):
        return self.value


class Address(BaseConfucius):
    user = models.ForeignKey(User, related_name='addresses')
    value = models.TextField()

    def __unicode__(self):
        return self.value


class Language(BaseConfucius):
    users = models.ManyToManyField(User, related_name='languages')
    code = models.CharField(max_length=5)
    value = models.CharField(max_length=25)

    def __unicode__(self):
        return self.value
