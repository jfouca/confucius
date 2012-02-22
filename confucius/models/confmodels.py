from django.contrib.auth.models import User
from django.db import models

from confucius.models import BaseConfucius


class Conference(BaseConfucius):
    class Meta:
        app_label = "confucius"

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
    users = models.ManyToManyField(User, through="ConferenceAccountRole")
    domains = models.ManyToManyField('Domain')

    def __unicode__(self):
        return self.title


class Alert(BaseConfucius):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference',)

    title = models.CharField(max_length=100, default=None)
    date = models.DateField()
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    def __unicode__(self):
        return self.title


class Role(BaseConfucius):
    class Meta:
        app_label = "confucius"
        unique_together = ('code',)

    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None)

    def __unicode__(self):
        return self.name


class ConferenceAccountRole(BaseConfucius):
    class Meta:
        app_label = "confucius"
        unique_together = ('user', 'conference')

    user = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    role = models.ManyToManyField('Role')
    domains = models.ManyToManyField('Domain')


class MessageTemplate(BaseConfucius):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference')

    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    def __unicode__(self):
        return self.title


class Domain(BaseConfucius):
    class Meta:
        app_label = "confucius"
        unique_together = ('code',)

    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None, verbose_name="Domain")

    def __unicode__(self):
        return self.name
