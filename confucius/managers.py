from base64 import b64encode
from datetime import datetime
from hashlib import sha1

from django.contrib.auth.models import User
from django.db import models


class AccountManager(models.Manager):
    def create(self, email, password, last_name, is_active=False):
        try:
            local, domain = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([local, domain.lower()])

        username = b64encode(sha1(email).digest())
        now = datetime.now()

        user = User(username=username, is_staff=False, is_active=is_active,
            is_superuser=False, last_login=now, date_joined=now)

        user.set_password(password)
        user.save(using=self._db)

        account = Account(user=user)
        account.save(using=self._db)

        email = EmailAddress(account=account, main=True)
        email.save(using=self._db)

        return account
