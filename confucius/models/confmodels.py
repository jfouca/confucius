from django.db import models
from confucius.models import Account, AccountManager
from django.contrib.auth.models import User
from django.core import validators
from django.db.models.signals import post_save

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
    domains = models.ManyToManyField('Domain')
    
    def __unicode__(self):
        return self.title


class Alert(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('title', 'conference',)

    title = models.CharField(max_length=100, default=None)
    date = models.DateField()
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)
    
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


class MockUser(models.Model):
    class Meta:
        app_label = "confucius"
        unique_together = ('original_president','original_conference')
    
    original_president = models.ForeignKey(Account, related_name="original_president")   
    original_conference = models.ForeignKey(Conference, related_name="original_conference")
    mock_conference = models.ForeignKey(Conference, related_name="mock_conference")

    def delete(self):
        """
        Firstly, delete all imitations : The relation (roles), the president, and the conference
        """
        ConferenceAccountRole.objects.get(account=self.original_president, conference=self.mock_conference).delete() #MockACR
        self.mock_conference.president.delete()     #MockPresident
        self.mock_conference.delete()               #MockConference
        super(MockUser, self).delete()
        
        
    def build_mock_user(self, president, conference, role):
        # Clean ex-Mock
        if len(MockUser.objects.filter(original_president = president, original_conference = conference)) > 0:
            MockUser.objects.get(original_president = president, mock_conference = conference).delete()
        
        """
        In order to build the mock, we must create a mock version of : 
            - The president
            - The conference
            - The relation (to add roles)
        """    
        # Build MockPresident
        email = ''.join(conference.title.split( )) + "@mockuser.com"
        mock_president = AccountManager().create(email, president.user.password, "Mock User", False)
        mock_president.save()

        # Build MockConference
        mock_conference = Conference.objects.get(pk=conference.pk)
        mock_conference.pk = None
        mock_conference.president = mock_president
        mock_conference.title = mock_conference.title+" (MockMode)"
        mock_conference.save()
        
        # Build MockCAR
        mock_car = ConferenceAccountRole.objects.create(account=president, conference=mock_conference)
        mock_car.role.add(role)
        
        # Build Mock
        mock_user = MockUser.objects.create(original_president = president, original_conference = conference, \
                mock_conference = mock_conference)    
        
        return mock_user
        
    
    def get_original_conference(self, president, mock_conference):
        if len(MockUser.objects.filter(original_president = president, mock_conference = mock_conference)) > 0:
            mock = MockUser.objects.get(original_president = president, mock_conference = mock_conference)
            return original_conference
        else:
            return None
    
    
    def check_user_is_in_mockmode(sender, **kwargs):
        """
        Check all "MockUsers" of a president: Delete them if they are not used (depends of the actual_conference field)
        """
        if not kwargs['instance']: return 
        account = kwargs['instance']
        
        # All MockUsers of a president
        mockusers_of_a_president = MockUser.objects.filter(original_president = account)    
        if len(mockusers_of_a_president) == 0: return
        
        # All MockUers of a president, which are not used
        mockusers_inactive = mockusers_of_a_president.exclude(mock_conference = account.actual_conference)
        if len(mockusers_inactive) == 0: return
            
        # Delete them
        for mock in mockusers_inactive:
            mock.delete()
        

    post_save.connect(check_user_is_in_mockmode, sender=Account)
