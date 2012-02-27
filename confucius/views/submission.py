from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import CreateView

from confucius.models import Paper
from confucius.forms import PaperForm
from confucius.views import RoleView


class CreatePaperView(RoleView, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = 'submission/paper_form.html'
    success_url = '/conference/dashboard/'

    def get_initial(self):
        initial = super(CreatePaperView, self).get_initial()
        initial.update({'conference': self.conference, 'submitter': self.request.user})
        return initial


@login_required
def submit_paper(request, pk_conference, pk_paper=None):
    if pk_paper is None:
        paper = None
    else:
        paper = Paper.objects.get(pk=pk_paper)

    form = PaperForm(instance=paper, pk_conference=pk_conference)

    if request.method == 'POST':    
        form = PaperForm(request.POST, request.FILES, instance=paper, pk_conference=pk_conference)

        if form.is_valid():
            paper = form.save(pk_conference=pk_conference, user=request.user)
            return redirect('dashboard')

    return render_to_response('submission/paper_form.html', {'form':form, 'instance':paper}, context_instance=RequestContext(request))

