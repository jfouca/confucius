from functools import wraps
from confucius.models import Conference, ConferenceUserRole
from django.shortcuts import redirect


def user_access_conference(onlyPresident=False, nameKwargConfId=None):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            return func(request, *args, **kwargs)
            """
            account = Account.objects.get(user=request.user)

            # if we want to use a request argument to get a conference...
            if nameKwargConfId and kwargs[nameKwargConfId]:
                conference = Conference.objects.get(pk=kwargs[nameKwargConfId])
            else:
                conference = account.actual_conference

            results = ConferenceUserRole.objects.filter(account=account, conference=conference)

            if conference and \
                    ((onlyPresident == False and len(results) == 1 and conference.isOpen) or conference.president == account):
                return func(request, *args, **kwargs)
            else:
                account.actual_conference = None
                account.save()
                return redirect('conferences')
            """
        return wraps(func)(inner_decorator)

    return decorator
