from base64 import b64encode
from django.contrib import messages
from django.core.mail import send_mail
from hashlib import sha1
import random
import string


def email_to_username(email):
    return b64encode(sha1(email).digest())


def errors_to_dict(form):
    errors = {}
    non_form_errors = {}

    try:
        if any(form.errors):
            errors = form.errors

        if any(form.non_form_errors()):
            non_form_errors = {
                form.prefix: form.non_form_errors()
            }
    except:
        pass

    return dict(errors + non_form_errors.items())


def random_string(size=64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for n in range(size))
    
    
def send_emails_to_group(receivers, title, content, request):
    for receiver in receivers:
        email = receiver.email
        try:
            send_mail("[Confucius Message] "+title, content, unicode(request.user.email), [unicode(email)], fail_silently=False)

        except:
            messages.error(request, u'An error occured during the email sending process. The SMTP settings may be uncorrect, or the receiver(%s) email address may not exist\n' % str(email))

    messages.success(request, u'You succesfully have just sent your email to the receiver(s)')
