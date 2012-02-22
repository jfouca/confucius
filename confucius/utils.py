from hashlib import sha1
from base64 import b64encode


def email_to_username(email):
    """
    Guaranteed to produce a 27 characters long string.
    """
    return b64encode(sha1(email).digest())
