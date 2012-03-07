from django.db import models

from confucius.models import Conference, ConfuciusModel, Domain, Language, User
import math

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
    file = models.FileField(upload_to='papers')

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
        marks_list = [assignment.review.overall_evaluation for assignment in assignments if assignment.has_review() ]
        try :
            average = self.stat_average(marks_list)
        except Exception as inst:
            return -1
        return int((average*100) / 7)
        
    def is_ambigous(self):
        assignments = self.assignments.all()
        marks_list = [assignment.review.overall_evaluation for assignment in assignments if assignment.has_review() ]
        try :
            variance = self.stat_variance(marks_list)
        except Exception as inst:
            return -1
        ecart_type = math.sqrt( variance )
        return ecart_type > 1.5
        
    
    def stat_variance(self, sample) :
        n = len( sample )
        mq = self.stat_average( sample )**2
        s = sum( [ x**2 for x in sample ] )
        variance = float(s) / n - mq
        return variance
        
    def stat_average(self, sample):
        if len(sample) < 1 :
            raise Exception('Sample length is not valid') 
        return float(sum(sample)) / len(sample) 
