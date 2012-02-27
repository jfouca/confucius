from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from confucius.forms import AlertForm, InvitationForm, DomainsForm
from confucius.models import Action, Alert, Conference, Event, Membership, Paper, Reminder, Role, Domain, ReviewerResponse, Assignment
from confucius.decorators.confdecorators import user_access_conference


from django.core.mail import send_mail


class MembershipListView(ListView):
    context_object_name = 'membership_list'
    template_name = 'conference/membership_list.html'

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user)


class ConferenceToggleView(SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Conference

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, *args, **kwargs):
        object = self.get_object()
        object.is_open = not object.is_open
        object.save()
        messages.success(self.request, 'You have successfully %s the conference %s' % ('opened' if object.is_open else 'closed', object.title))
        return redirect('dashboard')

def switch_to_last_accedeed(conf_pk, user):
    if conf_pk:
        conference = get_object_or_404(Conference, pk=conf_pk)
        membership = Membership.objects.get(conference=conference, user=user)
        membership.set_last_accessed()
    else:
        try:
            membership = Membership.objects.get(user=user, last_accessed=True)
            conference = membership.conference
        except Membership.DoesNotExist:
            messages.warning(request, 'You must select a conference first before accessing the dashboard')
            return redirect('membership_list')
    return conference            
            

@login_required
def dashboard(request, conference_pk=None, template_name='conference/dashboard.html'):

    conference = switch_to_last_accedeed(conference_pk, request.user)
    membership = Membership.objects.get(conference=conference, user=request.user)
    
    alerts_trigger = Alert.objects.filter(conference=conference.pk, reminder__isnull=True, action__isnull=True)
    alerts_reminder = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, action__isnull=True)
    alerts_action = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, reminder__isnull=True)

    user_papers = Paper.objects.filter(conference=conference, submitter=request.user).order_by('-last_update_date')
    user_assignments = Assignment.objects.filter(reviewer=request.user, is_assigned=True)
    
    chair_role = Role.objects.get(code="C")
    conference_reviews = Assignment.objects.filter(paper__conference=conference, is_done=True, review__isnull=False).order_by('-review__last_update_date')[:10]
    conference_papers = Paper.objects.filter(conference=conference).order_by('-submission_date')[:10]

    context = {
        'alerts_trigger': alerts_trigger,
        'alerts_reminder': alerts_reminder,
        'alerts_action': alerts_action,
        'conference': conference,
        'membership': membership,
        'user_papers': user_papers,
        'conference_papers': conference_papers,
        'user_assignments': user_assignments,
        'conference_reviews': conference_reviews
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


class ConferenceUpdateView(UpdateView):
    context_object_name = 'conference'
    form_class = modelform_factory(Conference, exclude=('members', 'is_open'))
    model = Conference
    success_url = '/conference/dashboard/'
    template_name = 'conference/conference_form.html'

'''
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

'''

@login_required
def create_alert(request, conference_pk, template_name='conference/alerts/create_alert.html'):
    
    conference = switch_to_last_accedeed(conference_pk, request.user)
    form = AlertForm()
    reminders = Reminder.objects.all()
    events = Event.objects.all()
    actions = Action.objects.all()

    if request.method == 'POST':
        form = AlertForm(request.POST, instance=Alert(conference=conference))
        if form.is_valid():
            alert = form.save()
            messages.success(request, 'Alert "%s" successfully created.' % alert.title)
            return redirect('dashboard')

    context = {
        'conference': conference,
        'form': form,
        'reminders': reminders,
        'events': events,
        'actions': actions
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


<<<<<<< HEAD
"""
Send a invitation email with an answer link for reviewer invitation
"""
@login_required
@user_access_conference(onlyPresident=True)
def reviewer_invitation(request, conference_pk=None):
    conference = get_object_or_404(Conference, pk=conference_pk)
    
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
      import datetime
      if datetime.date.today() > response.conference.reviews_end_date:
        return render_to_response('conference/reviewer_answer.html',
            {"error_message":"Paper Review is over for the conference "+response.conference.title}, 
            context_instance=RequestContext(request)) 
       
      #form = DomainsForm(instance=response.conference)
      if request.POST:
        if 'Accept' in request.POST:
            #domains_form = DomainsForm(request.POST, instance=response.conference)
            #if domains_form.is_valid():
            #    domains = domains_form.cleaned_data['domains']
            
            #Role creation and adding selected domain
            try :
                MembershipRole = Membership.objects.get(user=user, conference=response.conference)
            except:
                MembershipRole = Membership.objects.create(user=user, conference=response.conference)
            reviewer_role = Role.objects.get(code="R")
            MembershipRole.roles.add(reviewer_role)
                
            #for domain in domains:
            #    reviewer_domain = Domain.objects.get(name=domain)
            #    MembershipRole.domains.add(reviewer_domain)
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
            {"title":response.conference.title}, context_instance=RequestContext(request))
=======
class EditAlert(UpdateView):
    context_object_name = 'alert'
    form_class = AlertForm
    model = Alert
    success_url = '/conference/dashboard/'
    template_name = 'conference/alerts/edit_alert.html' 
    
class DeleteAlert(DeleteView):
    context_object_name = 'alert'
    form_class = AlertForm
    model = Alert
    success_url = '/conference/dashboard/'
    template_name = 'conference/alerts/confirm_delete_alert.html'
    
>>>>>>> 224597fc16a07cccf814e23c274d91138de40a88
