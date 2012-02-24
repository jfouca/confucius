from base64 import b64encode
from hashlib import sha1


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
