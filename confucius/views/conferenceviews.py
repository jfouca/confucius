from confucius.models import Conference, Role, ConferenceAccountRole, Account, Alert

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime

from confucius.forms import CreateAdminForm


@login_required
def duplicate_conference(request, conference_id, new_owner_pk, new_title):
    pass
    

@login_required
def detail_conference(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    return render_to_response('conf_detail.html', {'conference': conference})


"""
Create a conference with default alerts
"""
@login_required
def create_conference(request):
    
    if request.POST:
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            conference_title = form.cleaned_data['title']
            owner_account_id = form.cleaned_data['account'].pk
            
            #testing account and role presence
            owner_account = get_object_or_404(Account, pk=owner_account_id)
            
            #Conference creation
            new_conference = Conference.objects.create(
                title=conference_title, 
                president=owner_account, 
                startConfDate=datetime.now(), 
                endConfDate=datetime.now(), 
                startSubmitDate=datetime.now(), 
                endSubmitDate=datetime.now(), 
                startEvaluationDate=datetime.now(), 
                endEvaluationDate=datetime.now())
            
            
            #Alerte Creation
            new_alert = Alert.objects.create(
                title= "Fisrt alert", 
                conference= new_conference, 
                content= "The fisrt alert of the conference", 
                date= datetime.now())
    
            new_alert.save()
            new_conference.save()
            new_account_role.save()
    
            return render_to_response('conference/conf_creation_confirm.html')
        #print account.pk
    
    else:
        form = CreateAdminForm()
    
    return render_to_response("conference/create_conference.html", {"form":form}, context_instance=RequestContext(request))
    
    
