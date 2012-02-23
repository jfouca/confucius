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
    submissions_start_date = models.DateField()
    submissions_end_date = models.DateField()
    reviews_start_date = models.DateField()
    reviews_end_date = models.DateField()
    url = models.URLField(blank=True)
    members = models.ManyToManyField(User, through='Membership')
    domains = models.ManyToManyField('Domain', related_name="conferences")
    
    

    def __unicode__(self):
        return self.title


class Domain(ConfuciusModel):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Membership(ConfuciusModel):
    user = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    roles = models.ManyToManyField('Role')
    domains = models.ManyToManyField(Domain)
    last_accessed = models.BooleanField(default=False)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('user', 'conference')

    def set_last_accessed(self):
        Membership.objects.filter(user=self.user, conference=self.conference).update(last_accessed=False)
        self.last_accessed = True
        self.save()


class MessageTemplate(ConfuciusModel):
    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference')

    def __unicode__(self):
        return self.title

'''
class MockUser(models.Model):
    from django.db.models.signals import post_save

    class Meta:
        app_label = "confucius"
        unique_together = ('original_president', 'original_conference')

    original_president = models.ForeignKey(User, related_name="original_president")
    original_conference = models.ForeignKey(Conference, related_name="original_conference")
    mock_conference = models.ForeignKey(Conference, related_name="mock_conference")

    def delete(self):
        """
        Firstly, delete all imitations : The relation (roles), the president, and the conference
        """
        Membership.objects.get(user=self.original_president, conference=self.mock_conference).delete()  # MockACR
        self.mock_conference.president.delete()     # MockPresident
        self.mock_conference.delete()               # MockConference
        super(MockUser, self).delete()

    def build_mock_user(self, president, conference, role):
        # Clean ex-Mock
        if len(MockUser.objects.filter(original_president=president, original_conference=conference)) > 0:
            MockUser.objects.get(original_president=president, mock_conference=conference).delete()

        """
        In order to build the mock, we must create a mock version of :
            - The president
            - The conference
            - The relation (to add roles)
        """
        # Build MockPresident
        email = ''.join(conference.title.split()) + "@mockuser.com"
        mock_president = User.create(email=email, last_name="Mock User", is_active=False)
        mock_president.set_password('a')
        mock_president.save()

        # Build MockConference
        mock_conference = Conference.objects.get(pk=conference.pk)
        mock_conference.pk = None
        mock_conference.president = mock_president
        mock_conference.title = mock_conference.title + " (MockMode)"
        mock_conference.save()

        # Build MockCAR
        mock_car = Membership.objects.create(account=president, conference=mock_conference)
        mock_car.role.add(role)

        # Build Mock
        mock_user = MockUser.objects.create(original_president=president, original_conference=conference, \
                mock_conference=mock_conference)

        return mock_user

    def get_original_conference(self, president, mock_conference):
        if len(MockUser.objects.filter(original_president=president, mock_conference=mock_conference)) > 0:
            mock = MockUser.objects.get(original_president=president, mock_conference=mock_conference)
            return mock.original_conference
        else:
            return None

    def check_user_is_in_mockmode(sender, **kwargs):
        """
        Check all "MockUsers" of a president: Delete them if they are not used (depends of the actual_conference field)
        """
        if not kwargs['instance']:
            return
        account = kwargs['instance']

        # All MockUsers of a president
        mockusers_of_a_president = MockUser.objects.filter(original_president=account)
        if len(mockusers_of_a_president) == 0:
            return

        # All MockUers of a president, which are not used
        mockusers_inactive = mockusers_of_a_president.exclude(mock_conference=account.actual_conference)
        if len(mockusers_inactive) == 0:
            return

        # Delete them
        for mock in mockusers_inactive:
            mock.delete()

    post_save.connect(check_user_is_in_mockmode, sender=User)

'''

class Role(ConfuciusModel):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=9)

    def __unicode__(self):
        return self.name
