from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Conference, ConferenceAccountRole

@login_required
def list_conference(request) :
        
        conferences_president = Conference.objects.filter(president=request.user)
        conferences_with_role = ConferenceAccountRole.objects.filter(account=request.user)
        return render_to_response('conference/list_conference.html', { 'conferences_president' : conferences_president ,'conferences_with_role' : conferences_with_role }, context_instance=RequestContext(request))
