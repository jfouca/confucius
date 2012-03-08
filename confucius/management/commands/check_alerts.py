from django.core.management.base import BaseCommand
from confucius.models import Alert, Membership
from django.core.mail import send_mail
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Checks all the alerts that needs to be sent at the current date'

    def handle(self, *args, **options):

        current_date = datetime.now()
        #To improve : find a way to select only active alerts --maybe add a "is_over" Field in Alert Model
        self.check_reminders(current_date)
        self.check_triggers(current_date)

    def check_reminders(self, current_date):
        alerts = Alert.objects.filter(trigger_date__isnull=True, action__isnull=True)
        for alert in alerts:
            conference = alert.conference
            event = alert.event.name
            delta = timedelta(days=-alert.reminder.value)
            date = conference.__getattribute__(event)
            new_date = date + delta
            self.do_task(alert, conference, new_date, current_date)

    def check_triggers(self, current_date):
        alerts = Alert.objects.filter(reminder__isnull=True, action__isnull=True)
        for alert in alerts:
            conference = alert.conference
            new_date = alert.trigger_date
            self.do_task(alert, conference, new_date, current_date)

    def do_task(self, alert, conference, new_date, current_date):
        for role in alert.roles.all():
            if str(new_date)[0:10] == str(current_date)[0:10]:
                membership = Membership.objects.filter(conference=conference, roles=role)
                for entry in membership:
                    user = entry.user
                    email = user.email
                    self.stdout.write(" ** envoi de mail a l adresse suivante: %s ** \n" % str(email))
                    try:
                        send_mail("[Confucius Alert] "+alert.title, alert.content, 'no-reply-alerts@confucius.com', [str(email)], fail_silently=False)
                    except:
                        self.stderr.write("An error occured during the email sending process. The SMTP settings may be uncorrect, or the receiver(%s) email address may not exist\n" % str(email))
