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
    
    accounts = models.ManyToManyField(Account, through="ConferenceAccountRole")
    domains = models.ManyToManyField('Domain')
        
    def __unicode__(self):
        return self.title
    

class Alert(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference',)

    title = models.CharField(max_length=100, default=None)
    trigger_date = models.DateField(verbose_name="trigger date", blank=True, null=True)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)
    reminder = models.ForeignKey('Reminder', blank=True, null=True)
    event = models.ForeignKey('Event', blank=True, null=True)
    action = models.ForeignKey('Action', blank=True, null=True)
    roles = models.ManyToManyField('Role', blank=True)
    forPresident = models.BooleanField()
    
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
        unique_together = ('account', 'conference')

    account = models.ForeignKey(Account)
    conference = models.ForeignKey(Conference)
    role = models.ManyToManyField('Role')
    domains = models.ManyToManyField('Domain')
    
class MessageTemplate(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference')

    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)
    
    def __unicode__(self):
        return self.title
        
class Domain(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('code',)

    code = models.CharField(max_length=4, default=None)
    name = models.CharField(max_length=50, default=None, verbose_name="Domain")
    
    def __unicode__(self):
        return self.name
        
class Reminder(models.Model):
    
    class Meta:
        app_label = "confucius"
        unique_together = ('value','name')

    value = models.PositiveIntegerField()
    name = models.CharField(max_length=155, verbose_name="reminder")
    
    def __unicode__(self):
        return self.name
    
class Event(models.Model):
    class Meta:
        app_label = "confucius"
        
    name = models.CharField(max_length=155, verbose_name="linked to")
    
    def __unicode__(self):
        return self.name
        
class Action(models.Model):
    class Meta:
        app_label = "confucius"
        
    name = models.CharField(max_length=155, verbose_name="Action")
    
    def __unicode__(self):
        return self.name      
    
    
    

    

