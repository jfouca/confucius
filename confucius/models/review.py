from django.contrib.auth.models import User
from django.db import models

from confucius.models import Conference, ConfuciusModel, Paper


class Assignment(ConfuciusModel):
    reviewer = models.ForeignKey(User)
    paper = models.ForeignKey('Paper')
    is_accepted = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)
    review = models.ForeignKey('Review', blank=True, null=True, related_name="assignment")
    
    class Meta(ConfuciusModel.Meta):
        unique_together = ('reviewer', 'paper',)
    
    def __unicode__(self):
        return str(self.reviewer) + " <=> " + str(self.paper)
    
      
    
class Review(ConfuciusModel):
    title = models.CharField(max_length=50)
    detailed_commentary = models.TextField()
    commentary_for_president = models.TextField()
    overall_evaluation = models.IntegerField()
    reviewer_confidence = models.IntegerField()
    last_update_date = models.DateField()
    
    def __unicode__(self):
        return self.title + " by " + self.assignment.reviewer 

    def save(self, *args, **kwargs):
        from datetime import datetime
            
        self.last_update_date = datetime.now()
        super(Review, self).save(*args, **kwargs)
      
