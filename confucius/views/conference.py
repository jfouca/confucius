from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from confucius.forms import AlertForm
from confucius.models import Action, Alert, Assignment, Conference, Event, Membership, Paper, Reminder, Role
from confucius.decorators.confdecorators import user_access_conference


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
    
