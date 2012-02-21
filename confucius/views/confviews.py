from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Conference, ConferenceAccountRole
from django.forms.models import modelform_factory

from confucius.decorators import user_in_conference
 

 
@login_required
@user_in_conference
def home_conference(request, conf_id): 
    return HttpResponse("<html><body>Ca marche.</body></html>")
 
 
@login_required
def list_conference(request) :
    conferences_president = Conference.objects.filter(president=request.user).filter(isOpen="True").order_by('endConfDate')
    conferences_with_role = ConferenceAccountRole.objects.filter(account=request.user).filter(conference__isOpen="True").order_by('conference__endConfDate')
    return render_to_response('conference/list_conference.html', { 'conferences_president' : conferences_president ,'conferences_with_role' : conferences_with_role }, context_instance=RequestContext(request))
        
@login_required
def edit_conference(request, conf_id) :
	
	ConferenceForm = modelform_factory(Conference, exclude=('accounts','title','president'))
	conference =  Conference.objects.get(pk=conf_id)
	if conference.president.user == request.user:
	  auth = "true"
	  print "is president"
	  if request.POST:
	    form = ConferenceForm(request.POST, instance=conference)
	    if form.is_valid():
	      form.save()
	  else:	    
	    form = ConferenceForm(instance=conference)
	    
	  return render_to_response("conference/edit_conference.html", {
         "auth": auth, "conf_id" : conf_id , "form" : form, "conference" : conference
	},context_instance=RequestContext(request))
	
	else:
	  
	  auth = "false" 
          return render_to_response("conference/edit_conference.html", {
          "conf_id" : conf_id , "auth" : auth, "conference" : conference
	},context_instance=RequestContext(request)) 

