from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Conference, ConferenceAccountRole
from django.forms.models import modelform_factory
 
 
@login_required
def list_conference(request) :
        
        conferences_president = Conference.objects.filter(president=request.user)
        conferences_with_role = ConferenceAccountRole.objects.filter(account=request.user)
        return render_to_response('conference/list_conference.html',
        { 'conferences_president' : conferences_president ,'conferences_with_role' : conferences_with_role },
        context_instance=RequestContext(request))

        
@login_required
def edit_conference(request, conf_id) :
	
	ConferenceForm = modelform_factory(Conference, exclude=('accounts','title','president'))
	conference =  Conference.objects.get(pk=conf_id)
	if conference.president.user == request.user:
	  print "is president"
	  if request.POST:

	    form = ConferenceForm(request.POST, instance=conference)
	    if form.is_valid():
	    #conference.title = form.cleaned_data['title']
	    #pass
	      form.save()
		# do something.
	  else:
	    
	    form = ConferenceForm(instance=conference)
	    auth = "true"
	    return render_to_response("conference/edit_conference.html", {
         "auth": auth, "conf_id" : conf_id , "form" : form, "conference" : conference
	},context_instance=RequestContext(request))
	
	else:
	  
	  auth = "false" 
          return render_to_response("conference/edit_conference.html", {
          "conf_id" : conf_id , "auth" : auth, "conference" : conference
	},context_instance=RequestContext(request)) 

	
     
      
      