from django.contrib.auth.decorators import user_passes_test

from functools import wraps
from confucius.models import Account, Conference, ConferenceAccountRole
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def user_access_conference(onlyPresident=False, nameKwargConfId=None):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            account = Account.objects.get(user=request.user)
            
            # if we want to use a request argument to get a conference...
            if nameKwargConfId and kwargs[nameKwargConfId]:
                conference = Conference.objects.get(pk=kwargs[nameKwargConfId])
            else:
                conference = account.actual_conference
                
            results = ConferenceAccountRole.objects.filter(account=account, conference=conference)

            if (onlyPresident == False and len(results) == 1 and conference.isOpen) or conference.president == account:
        	    return func(request, *args, **kwargs)
            else:
                account.actual_conference = None
                account.save()
                return redirect('conferences') 

        return wraps(func)(inner_decorator)

    return decorator
