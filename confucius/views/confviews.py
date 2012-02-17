from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Conference, ConferenceAccountRole

@login_required
def list_conference(request) :
        
        conferences_president = Conference.objects.filter(president=request.user).filter(isOpen="True").order_by('endConfDate')
        conferences_with_role = ConferenceAccountRole.objects.filter(account=request.user).filter(conference__isOpen="True").order_by('conference__endConfDate')
        return render_to_response('conference/list_conference.html', { 'conferences_president' : conferences_president ,'conferences_with_role' : conferences_with_role }, context_instance=RequestContext(request))
