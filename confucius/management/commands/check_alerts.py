from django.core.management.base import BaseCommand, CommandError
from confucius.models import Conference, Account, Role, Alert, Reminder, Event, ConferenceAccountRole, EmailAddress
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
            self.do_task(alert,conference,new_date,current_date)
    
    def check_triggers(self, current_date):
        alerts = Alert.objects.filter(reminder__isnull=True, action__isnull=True)
        for alert in alerts:
            conference = alert.conference
            new_date = alert.trigger_date
            self.do_task(alert,conference,new_date,current_date)    
    
    def do_task(self, alert, conference, new_date, current_date):
        #Config properly SMTP server
        host = 'y.lemaulf@orange.fr'
        passwd = 'lemaulf'
        if alert.forPresident == True:
            president_email = EmailAddress.objects.get(account=conference.president,main=True)
            send_mail(alert.title+" to president", alert.content+"-- to president", 'no-reply-alerts@confucius.com',[str(president_email)], fail_silently=False, auth_user=host, auth_password=passwd)
        for role in alert.roles.all() :
            if str(new_date)[0:10] == str(current_date)[0:10]:
                confaccountrole = ConferenceAccountRole.objects.filter(conference=conference,role=role)
                for entry in confaccountrole:
                    account = entry.account
                    email = EmailAddress.objects.get(account=account,main=True)
                    send_mail(alert.title, alert.content, 'no-reply-alerts@confucius.com',[str(email)], fail_silently=False, auth_user=host, auth_password=passwd)
                        
                        
