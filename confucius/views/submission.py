from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.forms.models import modelform_factory
from django.template import RequestContext
from confucius.models import Paper, Membership, Conference
from confucius.forms import PaperForm


@login_required
def submit_paper(request, pk_conference, pk_paper=None):
    if pk_paper is None:
        form = PaperForm(pk_conference=pk_conference)
    else:
        paper = Paper.objects.get(pk=pk_paper)
        form = PaperForm(instance=paper, pk_conference=pk_conference)
    
    
    if request.method == 'POST':    
        if pk_paper is None:
            form = PaperForm(request.POST, request.FILES, pk_conference=pk_conference)
        else:
            paper = Paper.objects.get(pk=pk_paper)
            form = PaperForm(request.POST, request.FILES, instance=paper, pk_conference=pk_conference)
        
        
        if form.is_valid():
            paper = form.save(pk_conference=pk_conference, user=request.user)
                
            return redirect('edit_paper', pk_conference, paper.pk)
    
    return render_to_response('submission/paper_form.html', {'form':form}, context_instance=RequestContext(request))

