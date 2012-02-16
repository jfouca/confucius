from confucius.models import Conference, Role, ConferenceAccountRole

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


@login_required
def create_conference(request, owner_id, conference_title):
    owner_user = get_object_or_404(Account, pk=president_id)
    
    #Conference creation
    new_conference = Conference.objects.(title=conference_title, president=owner_user, startConfDate=datetime.now(), endConfDate=datetime.now(), startSubmitDate=datetime.now(), endSubmitDate=datetime.now(), startEvaluationDate=datetime.now(), endEvaluationDate=datetime.now())
    
    #ConferenceAccountRole "President" creation for the owner of the conference
    president_role = Role.objects.get(code="PRESIDENT")
    account_role = ConferenceAccountRole.objects.create(account=owner_user, role=president_role)
    
    #Alerte Creation
    #No alert creation at this time
    
    new_conference.save()
    account_role.save()
    
    return render_to_response('conf_creation_confirm.html')


@login_required
def duplicate_conference(request, conference_id, new_title):
    pass
    

@login_required
def detail_conference(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    return render_to_response('conf_detail.html', {'conference': conference})

    
    
