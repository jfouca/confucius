import datetime
from django import forms
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from confucius.models import Conference, ConferenceAccountRole, Account, Role, ReviewerResponse, Domain
from confucius.forms import EditConfForm, InviteReviewerForm, DomainsForm 
from django.forms.models import modelform_factory
from django.core.mail import send_mail

from confucius.decorators import user_access_conference

from confucius.utils import email_to_username

 
@login_required
@user_access_conference()
def home_conference(request):
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference
    
    directory = "conference/home/"
    if conference.president == account:
        roles = ()
        template = "conf_PRES.html"
        #Pour le livrable 3, voir 4, il faudra creer des listes d'evaluation, de soumissions et d'alertes 
    else:
        roles = ConferenceAccountRole.objects.get(conference=conference, account=account).role.all()
        template = "conf_AUTHREVI.html"
    
    
    return render_to_response(directory+template, {'conference' : conference, 'roles': roles, 'rolesCode': [role.code for role in roles]}, context_instance=RequestContext(request))


@login_required
@user_access_conference(nameKwargConfId='conf_id')
def change_conference(request, conf_id):
    conference = Conference.objects.get(pk=conf_id)
    account = Account.objects.get(user=request.user)
    account.actual_conference = conference
    account.save()
    
    return redirect('home_conference')


@login_required
@user_access_conference(onlyPresident=True)
def close_conference(request):
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference
        
    if request.method == 'POST':
        conference.isOpen = False
        conference.save()
        return render_to_response('conference/confirm_close_conference.html', {'conference':conference}, context_instance=RequestContext(request))
    return render_to_response('conference/close_conference.html', {'conference':conference}, context_instance=RequestContext(request))



@login_required
@user_access_conference(onlyPresident=True)
def open_conference(request):
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference
        
    if request.method == 'POST':
        conference.isOpen = True
        conference.save()
        return render_to_response('conference/confirm_open_conference.html', {'conference':conference}, context_instance=RequestContext(request))
    return render_to_response('conference/open_conference.html', {'conference':conference}, context_instance=RequestContext(request))


 
@login_required
def list_conference(request) :
    conferences_president = Conference.objects.filter(president=request.user).order_by('endConfDate')
    conferences_with_role = ConferenceAccountRole.objects.filter(account=request.user).filter(conference__isOpen="True").order_by('conference__endConfDate')
    return render_to_response('conference/list_conference.html', { 'conferences_president' : conferences_president ,'conferences_with_role' : conferences_with_role }, context_instance=RequestContext(request))



@login_required
@user_access_conference(onlyPresident=True)
def edit_conference(request) :
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference
    form = EditConfForm()

    if conference.president.user == request.user:
        auth = "true"
        print "is president"
        if request.POST:
            form = EditConfForm(request.POST, instance=conference)
            if form.is_valid():
                form.save()   
        else:	    
            form = EditConfForm(instance=conference)

        return render_to_response("conference/edit_conference.html", {
        "auth": auth, "conf_id" : conference.pk , "form" : form, "conference" : conference
        },context_instance=RequestContext(request))

    else:
        auth = "false" 
        return render_to_response("conference/edit_conference.html", {
        "conf_id" : conf_id , "auth" : auth, "conference" : conference
        },context_instance=RequestContext(request)) 

    auth = "true"
    return render_to_response("conference/edit_conference.html", {
    "auth": auth, "conf_id" : conf_id , "form" : form, "conference" : conference
    },context_instance=RequestContext(request))


"""
Send a invitation mail with an answer link for reviewer nomination
"""
@login_required
@user_access_conference(onlyPresident=True)
def invite_reviewer(request):
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference
    
    if request.POST:
        form = InviteReviewerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            hash_code = email_to_username(email)
            # Adding the invitation to the answer wait table with non duplication test
            try:
                response = ReviewerResponse.objects.create(hash_code=hash_code, email_addr=email, conference=conference, invitation_status="W")
            except IntegrityError:
                form.error_messages = "An invitation already exist for the email address "+email
                return render_to_response('conference/invite_reviewer.html',{"form":form}, context_instance=RequestContext(request))
            
            # Sending a mail to the requested email address
            send_mail('Confucius Reviewer Invitation', 'You just have receive an invitation to be reviewer for the conference '+conference.title +'<br> Please find enclose a link to answer this invitation : http://localhost:8000/conference/reviewer/'+hash_code, 'no-reply@confucius.com',[email], fail_silently=False)
            
            return render_to_response("conference/invite_reviewer_confirm.html",{"email": email},context_instance=RequestContext(request))   
    else:
        form = InviteReviewerForm()
        form.error_messages = None
        return render_to_response("conference/invite_reviewer.html",{"form":form}, context_instance=RequestContext(request))


"""
When a potential reviewer click on the answer link
"""    
@login_required(login_url='/action/login/')
def reviewer_invitation_response(request, hashCode):
      
      print hashCode
      account = Account.objects.get(user=request.user)
      
      assert hashCode is not None
      
      # Test if the key inside the answer link is in the answer wait table
      try:
        response = ReviewerResponse.objects.get(hash_code=hashCode)
      except ReviewerResponse.DoesNotExist:
        return render_to_response('conference/reviewer_answer.html',
            {"error_message":"The provided Response code is unknown"}, 
            context_instance=RequestContext(request))
      
      # Test if the conference paper review is not over
      if datetime.date.today() > response.conference.endEvaluationDate:
        return render_to_response('conference/reviewer_answer.html',
            {"error_message":"Paper Review is over for the conference "+response.conference.title}, 
            context_instance=RequestContext(request)) 
       
      form = DomainsForm(instance=response.conference)
      if request.POST:
        if 'Accept' in request.POST:
            domains_form = DomainsForm(request.POST, instance=response.conference)
            if domains_form.is_valid():
                domains = domains_form.cleaned_data['domains']
            
            #Role creation and adding selected domain
            confAccountRole = ConferenceAccountRole.objects.create(account=account, conference=response.conference)
            reviewer_role = get_object_or_404(Role, code="REVI")
            confAccountRole.role.add(reviewer_role)
            for domain in domains:
                reviewer_domain = get_object_or_404(Domain, name=domain)
            #Delete the current key from the answer wait table
            response.delete()
            return render_to_response('conference/reviewer_answer_confirm.html', context_instance=RequestContext(request))
        if 'Refuse' in request.POST:
            #Pass the status of the answer to "Refused"
            response.invitation_status="R"
            response.save()
            return render_to_response('conference/reviewer_answer_confirm.html', context_instance=RequestContext(request))    
      else:
        return render_to_response('conference/reviewer_answer.html',
            {"title":response.conference.title, "form":form}, context_instance=RequestContext(request))
