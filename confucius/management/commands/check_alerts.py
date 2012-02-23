from django.core.management.base import BaseCommand, CommandError
from confucius.models import Conference, Account, Role, Alert, Reminder, Event, ConferenceAccountRole, EmailAddress
from django.core.mail import send_mail
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Checks all the alerts that needs to be sent at the current date'

    def handle(self, *args, **options):
        current_date = datetime.now()
        #To improve : find a way to select only active alerts --maybe add a "is_over" Field in Alert Model
        alerts = Alert.objects.filter(trigger_date__isnull=True)
        for alert in alerts:
            conference = alert.conference
            event = alert.event.name
            delta = timedelta(days=-alert.reminder.value)
            date = conference.__getattribute__(event)
            new_date = date + delta
            for role in alert.roles.all() :
                if str(new_date)[0:10] == str(current_date)[0:10]:
                    confaccountrole = ConferenceAccountRole.objects.filter(conference=conference,role=role)
                    for entry in confaccountrole:
                        account = entry.account
                        email = EmailAddress.objects.get(account=account,main=True)
                        send_mail(alert.title, alert.content, 'no-reply-alerts@confucius.com',str(email), fail_silently=False)
