from django.db import models
from confucius.models import Account
from django.core import validators

class Conference(models.Model):
    class Meta:
        app_label = "confucius"

    title = models.CharField(max_length=100, unique=True, default=None)
    isOpen = models.BooleanField(default='False')
    startConfDate = models.DateField()
    endConfDate = models.DateField()
    startSubmitDate = models.DateField()
    endSubmitDate = models.DateField()
    startEvaluationDate  = models.DateField()
    endEvaluationDate = models.DateField()
    
    url = models.URLField(blank=True)
    president = models.ForeignKey(Account, related_name="president")
    
    accounts = models.ManyToManyField(Account, through="ConferenceAccountRole", related_name="conf_to_account")
        
    def __unicode__(self):
        return self.title
    

class Alert(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference',)

    title = models.CharField(max_length=100, default=None)
    date = models.DateField()
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)
    
    def __unicode__(self):
        return self.title


class Role(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('code',)

    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None)
    
    def __unicode__(self):
        return self.name


class ConferenceAccountRole(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('account', 'conference',)

    account = models.ForeignKey(Account)
    conference = models.ForeignKey(Conference)
    role = models.ManyToManyField(Role)

    
class MessageTemplate(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference')

    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)
    
    def __unicode__(self):
        return self.title


