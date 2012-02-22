from django.views.generic import UpdateView, ListView

from confucius.forms import ConferenceForm
from confucius.models import Conference, Membership


class MembershipListView(ListView):
    context_object_name = 'membership_list'
    template_name = 'conference/membership_list.html'

    def get_queryset(self):
        return Membership.objects.filter(user__exact=self.request.user)


class ConferenceUpdateView(UpdateView):
    context_object_name = 'conference'
    form_class = ConferenceForm
    model = Conference
    success_url = '/conference/'
    template_name = 'conference/conference_form.html'
