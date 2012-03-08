from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from confucius.models.conference import my_send_mail
from confucius.models import Alert, ConfuciusModel, User, Conference, Membership


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
    detailed_commentary = models.TextField(verbose_name="Public commentary")
    commentary_for_president = models.TextField(blank=True, verbose_name="Chairman commentary only")
    overall_evaluation = models.IntegerField()
    reviewer_confidence = models.IntegerField()
    last_update_date = models.DateField(default=datetime.now())

    def __unicode__(self):
        return self.title + " by " + self.assignment.reviewer

    def save(self, *args, **kwargs):
        self.last_update_date = datetime.now()
        super(Review, self).save(*args, **kwargs)
        
    def get_assignment(self):
        return self.assignment.all()[0]


class PaperSelection(ConfuciusModel):
    paper = models.OneToOneField('Paper', related_name="selection")
    conference = models.ForeignKey('Conference', related_name="selections")
    is_selected = models.BooleanField(default=False)
    is_submit = models.BooleanField(default=False)
    
@receiver(pre_save, sender=Assignment, dispatch_uid="Assignment_identifier")
def my_review_handler(sender, instance, **kwargs):
    if instance.pk is None or instance.is_done == False:
        return
    conference = instance.conference
    alerts = Alert.objects.filter( action=3, conference = conference )
    for alert in alerts:
        my_send_mail(alert,conference)
