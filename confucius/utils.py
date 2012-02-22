from hashlib import sha1
from base64 import b64encode


def email_to_username(email):
    return b64encode(sha1(email).digest())
