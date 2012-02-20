from django.contrib.auth.models import User

from confucius.models import Account


class AccountBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        try:
            account = Account.objects.get_by_email(username)
            if account.user.is_active and account.check_password(password):
                return account.user
        except Account.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
