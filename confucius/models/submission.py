from django.contrib.auth.models import User
from django.db import models
from confucius.models import Domain

from confucius.models import ConfuciusModel

class Paper(ConfuciusModel):
    title = models.CharField(max_length=100, unique=True)
    submitter = models.ForeignKey(User)
    emails_authors = models.TextField()
    submission_date = models.DateField()
    last_update_date = models.DateField()
    language = models.ForeignKey('Language')
    domains = models.ManyToManyField('Domain')
    conference = models.ForeignKey('Conference')
    document = models.FileField(upload_to="documents")
          
    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference',)
   
    def __unicode__(self):
        return self.title


    def save(self, *args, **kwargs):
        from datetime import datetime
        if self.pk is None:
            self.submission_date = datetime.now()
        self.last_update_date = datetime.now()
        super(Paper, self).save(*args, **kwargs)
