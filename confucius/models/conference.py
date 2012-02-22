from django.contrib.auth.models import User
from django.db import models

from confucius.models import ConfuciusModel


class Alert(ConfuciusModel):
    title = models.CharField(max_length=100, default=None)
    date = models.DateField()
    content = models.TextField(default=None)
    conference = models.ForeignKey('Conference')

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference',)

    def __unicode__(self):
        return self.title


class Conference(ConfuciusModel):
    title = models.CharField(max_length=100, unique=True)
    is_open = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    submissions_start_date = models.DateField()
    submissions_end_date = models.DateField()
    reviews_start_date = models.DateField()
    reviews_end_date = models.DateField()
    url = models.URLField(blank=True)
    president = models.ForeignKey(User, related_name='chaired_conferences')
    users = models.ManyToManyField(User, through='Role')
    domains = models.ManyToManyField('Domain')

    def __unicode__(self):
        return self.title


class Domain(ConfuciusModel):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class MessageTemplate(ConfuciusModel):
    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference')

    def __unicode__(self):
        return self.title


class Role(ConfuciusModel):
    user = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    role = models.CharField(max_length=1,
        choices=(
            ('C', 'Chair'),
            ('R', 'Reviewer'),
            ('S', 'Submitter'),
    ))
    domains = models.ManyToManyField(Domain)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('user', 'conference')
