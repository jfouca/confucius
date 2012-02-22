from django.contrib.auth.models import User
from django.db import models

from confucius.models import BaseConfucius


class Conference(BaseConfucius):
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


class Alert(BaseConfucius):
    title = models.CharField(max_length=100, default=None)
    date = models.DateField()
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    class Meta(BaseConfucius.meta):
        unique_together = ('title', 'conference',)

    def __unicode__(self):
        return self.title


class Role(BaseConfucius):
    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None)

    def __unicode__(self):
        return self.name


class ConferenceAccountRole(BaseConfucius):
    account = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    role = models.ManyToManyField('Role')
    domains = models.ManyToManyField('Domain')

    class Meta(BaseConfucius.Meta):
        unique_together = ('account', 'conference')


class MessageTemplate(BaseConfucius):
    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    class Meta(BaseConfucius.Meta):
        unique_together = ('title', 'conference')

    def __unicode__(self):
        return self.title


class Domain(BaseConfucius):
    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None, verbose_name="Domain")

    class Meta(BaseConfucius.Meta):
        unique_together = ('code',)

    def __unicode__(self):
        return self.name
