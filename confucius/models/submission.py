from django.db import models

from confucius.models import Conference, ConfuciusModel, Domain, Language, User


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
    
