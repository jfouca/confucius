from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import UpdateView, ListView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from confucius.forms import AlertForm, InvitationForm
from confucius.models import Action, Alert, Conference, Event, Membership, MockUser, Reminder, Role, ReviewerResponse
from confucius.decorators.confdecorators import user_access_conference


from django.core.mail import send_mail


class MembershipListView(ListView):
    context_object_name = 'membership_list'
    template_name = 'conference/membership_list.html'

    def get_queryset(self):
        return Membership.objects.filter(user__exact=self.request.user)


class ConferenceToggleView(SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Conference

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, *args, **kwargs):
        object = self.get_object()
        object.is_open = not object.is_open
        object.save()
        return redirect('/conference/')


def update_dashboard(request, conference_pk):
    Membership.objects.get(user=request.user.pk, conference=conference_pk).set_last_accessed()
    return redirect('dashboard')


class ConferenceUpdateView(UpdateView):
    context_object_name = 'conference'
    form_class = modelform_factory(Conference, exclude=('members', 'is_open'))
    model = Conference
    success_url = '/conference/'
    template_name = 'conference/conference_form.html'


@login_required
@user_access_conference(onlyPresident=True)
def use_mockuser(request, role_id):
    president = request.user
    conference = president.actual_conference

    mock_user = MockUser().build_mock_user(president, conference, Role.objects.get(pk=role_id))

    return redirect('change_conference', mock_user.mock_conference.pk)


@login_required
@user_access_conference()
def exit_mockuser(request):
    president = request.user
    mock_conference = president.actual_conference

    mock_user = MockUser.objects.get(original_president=president, mock_conference=mock_conference)
    original_conference = mock_user.original_conference

    return redirect('change_conference', original_conference.pk)


@login_required
@user_access_conference()
def home_conference(request):
    conference = Membership.objects.get(user__exact=request.user, last_accessed=True).conference
    directory = "conference/home/"
    if request.user is conference.get_president():
        roles = ()
        template = "conf_PRES.html"
        alerts_trigger = Alert.objects.filter(conference=conference.pk, reminder__isnull=True, action__isnull=True)
        alerts_reminder = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, action__isnull=True)
        alerts_action = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, reminder__isnull=True)

        return render_to_response(directory + template, {'conference': conference, 'roles': roles, 'rolesCode': [role.code for role in roles], 'alerts_trigger': alerts_trigger, 'alerts_reminder': alerts_reminder, 'alerts_action': alerts_action}, context_instance=RequestContext(request))
        # Pour le livrable 3, voir 4, il faudra creer des listes d'evaluation, de soumissions et d'alertes
    else:
        roles = Membership.objects.get(conference=conference, user=request.user).roles.all()
        template = "conf_AUTHREVI.html"
        return render_to_response(directory + template, {'conference': conference, 'roles': roles, 'rolesCode': [role.code for role in roles]}, context_instance=RequestContext(request))


@login_required
@user_access_conference(onlyPresident=True)
def create_alert(request):
    conference = Membership.objects.get(user__exact=request.user, last_accessed=True).conference
    form = AlertForm(auto_id=True)
    reminders = Reminder.objects.all()
    events = Event.objects.all()
    actions = Action.objects.all()

    if request.method == 'POST':
        form = AlertForm(request.POST, instance=Alert(conference=conference))
        if form.is_valid():
            new_alert = form.save()
            return render_to_response('conference/alert/confirm_create_alert.html', {'alert': new_alert}, context_instance=RequestContext(request))

    return render_to_response('conference/alert/create_alert.html', {'conference': conference, 'alert_form': form, 'reminders': reminders, 'events': events, 'actions': actions}, context_instance=RequestContext(request))


"""
Send a invitation email with an answer link for reviewer invitation
"""
@login_required
@user_access_conference(onlyPresident=True)
def reviewer_invitation(request):
    conference = Membership.objects.get(user__exact=request.user, last_accessed=True).conference
    
    if request.POST:
        form = InvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            text = form.cleaned_data['invitation_text']
            
            from confucius.utils import email_to_username
            hash_code = email_to_username(email)
            # Adding the invitation to the answer wait table with non duplication test
            from django.db import IntegrityError
            try:
                response = ReviewerResponse.objects.create(hash_code=hash_code, email_addr=email, conference=conference, invitation_status="W")
            except IntegrityError:
                error_messages = "An invitation already exist for the email address "+email
                return render_to_response('conference/invite_reviewer.html',{"form":form,"error":error_messages}, context_instance=RequestContext(request))
            
            # Sending a mail to the requested email address
            send_mail('Confucius Reviewer Invitation',text+'http://localhost:8000/conference/reviewer_invitation/'+hash_code, 'no-reply@confucius.com',[email], fail_silently=False)
            
            return render_to_response("conference/invite_reviewer_confirm.html",{"email": email},context_instance=RequestContext(request))   
    else:
        text = 'You just have receive an invitation to be reviewer for the conference '+conference.title +'.Please find enclose a link to answer this invitation.'
        form = InvitationForm({'invitation_text':text})
        return render_to_response("conference/invite_reviewer.html",{"form":form}, context_instance=RequestContext(request))


"""
When a potential reviewer click on the answer link
"""    
@login_required(login_url='/account/action_login/')
def reviewer_response(request, hashCode):
      
      assert hashCode is not None
      user = request.user
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
