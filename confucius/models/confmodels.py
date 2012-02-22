from django.contrib.auth.models import User
from django.db import models

from confucius.models import ConfuciusModel


class Conference(ConfuciusModel):
    title = models.CharField(max_length=100, unique=True, default=None)
    isOpen = models.BooleanField(default='False')
    startConfDate = models.DateField()
    endConfDate = models.DateField()
    startSubmitDate = models.DateField()
    endSubmitDate = models.DateField()
    startEvaluationDate = models.DateField()
    endEvaluationDate = models.DateField()
    url = models.URLField(blank=True)
    president = models.ForeignKey(User, related_name="president")
    accounts = models.ManyToManyField(User, through="ConferenceAccountRole")
    domains = models.ManyToManyField('Domain')

    def __unicode__(self):
        return self.title


class Alert(ConfuciusModel):
    title = models.CharField(max_length=100, default=None)
    date = models.DateField()
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference',)

    def __unicode__(self):
        return self.title


class Role(ConfuciusModel):
    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None)

    def __unicode__(self):
        return self.name


class ConferenceAccountRole(ConfuciusModel):
    account = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    role = models.ManyToManyField('Role')
    domains = models.ManyToManyField('Domain')

    class Meta(ConfuciusModel.Meta):
        unique_together = ('account', 'conference')


class MessageTemplate(ConfuciusModel):
    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference')

    def __unicode__(self):
        return self.title


class Domain(ConfuciusModel):
    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None, verbose_name="Domain")

    class Meta(ConfuciusModel.Meta):
        unique_together = ('code',)

    def __unicode__(self):
        return self.name
