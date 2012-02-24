from base64 import b64encode
from hashlib import sha1


def email_to_username(email):
    return b64encode(sha1(email).digest())
