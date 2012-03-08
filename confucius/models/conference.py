from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from datetime import datetime
from confucius.models import ConfuciusModel, User


class Action(ConfuciusModel):
    name = models.CharField(max_length=155, verbose_name='Action')

    def __unicode__(self):
        return self.name


class Alert(ConfuciusModel):
    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey('Conference')
    trigger_date = models.DateField(verbose_name='trigger date', blank=True, null=True)
    reminder = models.ForeignKey('Reminder', blank=True, null=True)
    event = models.ForeignKey('Event', blank=True, null=True)
    action = models.ForeignKey('Action', blank=True, null=True)
    roles = models.ManyToManyField('Role', blank=True)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference',)

    def __unicode__(self):
        return self.title


class Conference(ConfuciusModel):
    title = models.CharField(max_length=100, unique=True)
    is_open = models.BooleanField(default=False)
    has_finalize_paper_selections = models.BooleanField(default=False)
    start_date = models.DateField()
    submissions_start_date = models.DateField()
    submissions_end_date = models.DateField()
    reviews_start_date = models.DateField()
    reviews_end_date = models.DateField()
    url = models.URLField(blank=True)
    members = models.ManyToManyField(User, through='Membership')
    domains = models.ManyToManyField('Domain', related_name='conferences')
    access_key = models.CharField(max_length=8)
    maximum_score = models.IntegerField(default=10)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('confucius.views.conference_access', (),
            {'conference_pk': self.pk, 'access_key': self.access_key})

    def save(self, *args, **kwargs):
        from confucius.utils import random_string

        if self.pk is None:
            self.access_key = random_string(8)

        super(Conference, self).save(*args, **kwargs)

    def are_submissions_over(self):
        return datetime.now().date() > self.submissions_end_date

    def are_submissions_notstarted(self):
        return datetime.now().date() < self.submissions_start_date

    def are_reviews_notstarted(self):
        return datetime.now().date() < self.reviews_start_date

    def are_reviews_over(self):
        return datetime.now().date() > self.reviews_end_date

    def is_started(self):
        return datetime.now().date() > self.start_date


class Domain(ConfuciusModel):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Event(ConfuciusModel):
    name = models.CharField(max_length=155, verbose_name='linked to')

    def __unicode__(self):
        return self.name


class Membership(ConfuciusModel):
    user = models.ForeignKey(User, related_name='memberships')
    conference = models.ForeignKey(Conference)
    roles = models.ManyToManyField('Role')
    domains = models.ManyToManyField(Domain)
    last_accessed = models.BooleanField(default=False)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('user', 'conference')

    def set_last_accessed(self):
        Membership.objects.filter(user=self.user).update(last_accessed=False)
        self.last_accessed = True
        self.save()

    def _has_role(self, code):
        try:
            self.roles.get(code=code)
            return True
        except:
            return False

    def has_chair_role(self):
        return self._has_role('C')

    def has_reviewer_role(self):
        return self._has_role('R')

    def has_submitter_role(self):
        return self._has_role('S')


@receiver(post_delete, sender=Membership, dispatch_uid="Membership_delete")
@receiver(pre_save, sender=Membership, dispatch_uid="Membership_identifier")
def my_user_handler(sender, instance, **kwargs):
    conference = instance.conference
    user_pre_save = instance.user
    alerts = Alert.objects.filter( (Q(action=1) | Q(action=2) ))
    for alert in alerts:
        if alert.action.pk == 1 and instance.pk is None :
            try:
                Membership.objects.get(conference=conference, user=user_pre_save)
            except:
                my_send_mail(alert,conference)
        elif alert.action.pk == 2 and instance.pk is not None:
            try:
                Membership.objects.get(conference=alert.conference, user=user_pre_save)
            except:
                my_send_mail(alert,conference)
                
                
def my_send_mail(alert, conference):
    from django.core.mail import send_mail
    for role in alert.roles.all():
        memberships_list = Membership.objects.filter(roles=role, conference=conference).all()
        users_email = [unicode(membership.user.email) for membership in memberships_list]
        try:
            send_mail("[Confucius Alert] "+alert.title, alert.content, 'no-reply-alerts@confucius.com', users_email, fail_silently=False)
        except:
            print "Error occured during email sending process. Please check your SMTP settings"
            

class MessageTemplate(ConfuciusModel):
    RECEIVER_CHOICES = (
        ('J', 'New User joined the Conference'),
        ('L', 'User left the Conference'),
        ('P', 'New paper has been submitted'),
        ('R', 'Review has been submitted'),
        ('S', 'Send Mail - Selected submitters'),
    )
    title = models.CharField(max_length=100, default=None)
    content = models.TextField(default=None)
    conference = models.ForeignKey(Conference, related_name="messages_templates")
    receiver = models.CharField(max_length=1, choices=RECEIVER_CHOICES)

    class Meta(ConfuciusModel.Meta):
        unique_together = ('title', 'conference')

    def __unicode__(self):
        return self.title


class Reminder(ConfuciusModel):
    value = models.PositiveIntegerField()
    name = models.CharField(max_length=155, verbose_name='reminder')

    class Meta(ConfuciusModel.Meta):
        unique_together = ('value', 'name')

    def __unicode__(self):
        return self.name


class Role(ConfuciusModel):
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=9)

    def __unicode__(self):
        return self.name


class Invitation(ConfuciusModel):
    user = models.ForeignKey(User)
    conference = models.ForeignKey(Conference)
    roles = models.ManyToManyField(Role)
    decision = models.CharField(max_length=1, choices=(
        ('A', 'Accepted'),
        ('R', 'Refused'),
        ('W', 'Waiting for response')
    ), default='W')
    key = models.CharField(max_length=64, unique=True)
    message = models.TextField()

    class Meta(ConfuciusModel.Meta):
        unique_together = ('user', 'conference')

    def _decision(self, code):
        self.decision = code
        self.save()

    def pending(self):
        return self.decision == 'W'

    def refuse(self):
        self._decision('R')

    def accept(self):
        self._decision('A')
