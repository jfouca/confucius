from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from confucius.forms import AlertForm
from confucius.models import Action, Alert, Assignment, Conference, Event, Membership, Paper, Reminder
from confucius.views import LoginRequiredView


class RoleView(LoginRequiredView):
    conference = None
    membership = None

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if pk:
            try:
                self.conference = Conference.objects.get(pk=pk)
            except:
                messages.warning(request, u'You have no membership to that conference.')
                return redirect('account')
        else:
            self.conference = request.user.get_last_accessed_conference()

        self.membership = Membership.objects.get(user=request.user, conference=self.conference)
        self.membership.set_last_accessed()

        if self.has_access(request):
            return super(RoleView, self).dispatch(request, *args, **kwargs)

        messages.warning(request, u'You have no access to that conference')
        return redirect('dashboard')

    def has_access(self, request):
        return True


class PresidentView(RoleView):
    def has_access(self, request):
        if not self.membership.has_chair_role():
            messages.warning(request, u'You are not chair for that conference')
            return False
        return True


class ReviewerView(RoleView):
    def has_access(self, request):
        if not self.membership.has_reviewer_role():
            messages.warning(request, u'You are not reviewer for that conference')
            return False
        return True


class SubmitterView(RoleView):
    def has_access(self, request):
        if not self.membership.has_submitter_role():
            messages.warning(request, u'You have no access to that conference')
            return False
        return True


class MembershipListView(ListView):
    context_object_name = 'membership_list'
    template_name = 'conference/membership_list.html'

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user)


class ConferenceToggleView(PresidentView, SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Conference

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, *args, **kwargs):
        object = self.get_object()
        object.is_open = not object.is_open
        object.save()
        messages.success(self.request, 'You have successfully %s the conference %s' % ('opened' if object.is_open else 'closed', object.title))
        return redirect('dashboard')


class DashboardView(TemplateView, RoleView):
    template_name = 'conference/dashboard.html'

    def get_context_data(self, **kwargs):
        conference = self.request.user.get_last_accessed_conference()
        membership = Membership.objects.get(conference=conference, user=self.request.user)
        alerts_trigger = Alert.objects.filter(conference=conference.pk, reminder__isnull=True, action__isnull=True)
        alerts_reminder = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, action__isnull=True)
        alerts_action = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, reminder__isnull=True)
        user_papers = Paper.objects.filter(conference=conference, submitter=self.request.user).order_by('-last_update_date')
        user_assignments = Assignment.objects.filter(reviewer=self.request.user, is_assigned=True)
        conference_reviews = Assignment.objects.filter(paper__conference=conference, is_done=True, review__isnull=False).order_by('-review__last_update_date')[:10]
        conference_papers = Paper.objects.filter(conference=conference).order_by('-submission_date')[:10]

        context = super(DashboardView, self).get_context_data(**kwargs)

        context.update({
            'alerts_trigger': alerts_trigger,
            'alerts_reminder': alerts_reminder,
            'alerts_action': alerts_action,
            'conference': conference,
            'membership': membership,
            'user_papers': user_papers,
            'conference_papers': conference_papers,
            'user_assignments': user_assignments,
            'conference_reviews': conference_reviews
        })

        return context


class ConferenceUpdateView(PresidentView, UpdateView):
    context_object_name = 'conference'
    form_class = modelform_factory(Conference, exclude=('members', 'is_open'))
    model = Conference
    success_url = '/conference/dashboard/'
    template_name = 'conference/conference_form.html'


@login_required
def create_alert(request, conference_pk, template_name='conference/alerts/create_alert.html'):
    return redirect('account')
    """
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
    """


class CreateAlertView(PresidentView, CreateView):
    context_object_name = 'alert'
    form_class = AlertForm
    model = Alert
    success_url = '/conference/dashboard/'
    template_name = 'conference/alerts/edit_alert.html'

    def get_initial(self):
        initial = super(CreateAlertView, self).get_initial()
        initial.update({'conference': self.conference})
        return initial


class EditAlert(PresidentView, UpdateView):
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
