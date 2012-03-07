from django.db import models

from confucius.models import Conference, ConfuciusModel, Domain, Language, User
import math
from confucius.extra import ContentTypeRestrictedFileField

class Paper(ConfuciusModel):
    title = models.CharField(max_length=100, unique=True)
    submitter = models.ForeignKey(User)
    co_authors = models.TextField(blank=True)
    description = models.TextField()
    submission_date = models.DateField(auto_now_add=True)
    last_update_date = models.DateField(auto_now=True)
    language = models.ForeignKey(Language)
    domains = models.ManyToManyField(Domain)
    conference = models.ForeignKey(Conference)
    file = ContentTypeRestrictedFileField(
        upload_to='paper',
        content_types=['application/pdf', 'application/msword' , 'application/postscript' , 'application/rtf', 'application/vnd.ms-powerpoint', 'image/jpeg', 'text/plain'],
        max_upload_size=5242880
    )
    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference',)

    def __unicode__(self):
        return self.title

    def get_assigned_assignments_count(self):
        return len([assignment for assignment in self.assignments.all() if assignment.is_assigned == True])

    def get_not_assigned_assignments_count(self):
        return len([assignment for assignment in self.assignments.all() if assignment.is_assigned == False])

    def get_mark(self):
        assignments = self.assignments.all()
        marks_list = [assignment.review.overall_evaluation for assignment in assignments if assignment.has_review() and assignment.is_done]
        try :
            average = self.stat_average(marks_list)
        except Exception as inst:
            return -1

        max_score = self.conference.maximum_score
        return int((average*100) / max_score)

    def get_reviewed_percent(self):
        total = self.assignments.all().count()
        value = self.assignments.filter(is_done=True).count()
        return value*100/total

    def is_ambigous(self):
        assignments = self.assignments.all()
        marks_list = [assignment.review.overall_evaluation for assignment in assignments if assignment.has_review() and assignment.is_done]
        try :
            variance = self.stat_variance(marks_list)
        except Exception as inst:
            return -1
        ecart_type = math.sqrt(variance)
        
        ecart_type_max = self.conference.maximum_score/4
        return ecart_type > ecart_type_max


    def stat_variance(self, sample):
        n = len(sample)
        mq = self.stat_average(sample)**2
        s = sum([x**2 for x in sample])
        variance = float(s) / n - mq
        return variance

    def stat_average(self, sample):
        if len(sample) < 1:
            raise Exception('Sample length is not valid')
        return float(sum(sample)) / len(sample)
