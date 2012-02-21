from django.contrib.auth.decorators import user_passes_test

from functools import wraps
from confucius.models import Account, Conference, ConferenceAccountRole
from django.shortcuts import render_to_response
from django.template import RequestContext
	
	
def user_in_conference():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
	    account = Account.objects.get(user=request.user)
	    conference = Conference.objects.get(pk=kwargs['conf_id'])
	    
	    if len(ConferenceAccountRole.objects.filter(account=account, conference=conference)) == 1 or conference.president == account:
		return func(request, *args, **kwargs)
	    else:
		return render_to_response("conference/no_access_conference.html",{},context_instance=RequestContext(request)) 

        return wraps(func)(inner_decorator)

    return decorator