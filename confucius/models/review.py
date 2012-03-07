from datetime import datetime
from django.db import models
from confucius.models import ConfuciusModel, User, Conference, Membership


class Assignment(ConfuciusModel):
    conference = models.ForeignKey(Conference, related_name="assignments")
    reviewer = models.ForeignKey(User, related_name="assignments")
    paper = models.ForeignKey('Paper', related_name="assignments")
    problem = models.TextField()
    is_assigned = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    review = models.ForeignKey('Review', blank=True, null=True, related_name="assignment")

    class Meta(ConfuciusModel.Meta):
        unique_together = ('reviewer', 'paper',)

    def __unicode__(self):
        return str(self.reviewer) + " <=> " + str(self.paper)

    def get_papers(self):
        return Assignment.objects.filter(conference=self.conference, reviewer=self.reviewer)

    def get_domains(self):
        return Membership.objects.get(conference=self.conference, user=self.reviewer).domains
        
    def has_review(self):
        if self.review is not None :
            return True
        return False


class Review(ConfuciusModel):
    detailed_commentary = models.TextField()
    commentary_for_president = models.TextField(blank=True)
    overall_evaluation = models.IntegerField()
    reviewer_confidence = models.IntegerField()
    last_update_date = models.DateField(default=datetime.now())

    def __unicode__(self):
        return self.title + " by " + self.assignment.reviewer

    def save(self, *args, **kwargs):
        self.last_update_date = datetime.now()
        super(Review, self).save(*args, **kwargs)


class PaperSelection(ConfuciusModel):
    paper = models.OneToOneField('Paper', related_name="selection")
    conference = models.ForeignKey('Conference', related_name="selections")
    is_selected = models.BooleanField(default=False)
    is_submit = models.BooleanField(default=False)
