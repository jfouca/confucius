from confucius.models import Conference, Membership, Role, User


class AccountBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.is_active and user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user, perm, obj=None):
        if not isinstance(obj, Conference):
            return True

        try:
            membership = Membership.objects.get(conference=obj, user=user)
        except Membership.DoesNotExist:
            return False

        chair = Role.objects.get(code='C')
        reviewer = Role.objects.get(code='R')
        submitter = Role.objects.get(code='S')

        if perm is 'change':
            if chair in membership.roles.all():
                return True
            return False
