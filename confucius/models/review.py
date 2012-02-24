from django.contrib.auth.models import User
from django.db import models

from confucius.models import Conference, ConfuciusModel, Paper

class Review(ConfuciusModel):
    reviewer = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    paper = models.ForeignKey(Paper)
    is_done = models.BooleanField(default=False)
    posted_date = models.DateField()
    last_update_date = models.DateField()
    detailed_commentary = models.TextField(default="Detailed commentary")
    commentary_for_president = models.TextField(default="Commentary for the president")
    overall_evaluation = models.IntegerField(default=0)
    reviewer_confidence = models.IntegerField(default=3)
   
    class Meta(ConfuciusModel.Meta):
        unique_together = ('reviewer', 'conference', 'paper',)
    
    def __unicode__(self):
        return self.title+" by "+self.reviewer

    def save(self, *args, **kwargs):
        from datetime import datetime
        if self.pk is None:
            self.creation_date = datetime.now()
        self.last_update_date = datetime.now()
        super(Review, self).save(*args, **kwargs)
      
