from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, ListView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from confucius.models import Conference, Membership


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
        return HttpResponseRedirect('/conference/')


class ConferenceUpdateView(UpdateView):
    context_object_name = 'conference'
    form_class = modelform_factory(Conference, exclude=('members', 'is_open'))
    model = Conference
    success_url = '/conference/'
    template_name = 'conference/conference_form.html'
