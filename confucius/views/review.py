from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from confucius.models import Assignment, Review, Paper
from confucius.views import dashboard
from confucius.forms import ReviewForm
from django.template import RequestContext


@login_required
def auto_assignment(request, pk_paper):
    paper = Paper.objects.get(pk=pk_paper)
    
    assignment = Assignment.objects.create(reviewer=request.user, paper=paper)
    assignment.save()
    
    return redirect('dashboard')
    
    
@login_required
def submit_review(request, pk_assignment):
    assignment = Assignment.objects.get(pk=pk_assignment)
    review = assignment.review
    form = ReviewForm(instance=review)

        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            review = form.save()
            assignment.review = review
            
            if request.POST.__contains__('save_and_submit'):
                assignment.is_done = True
            
            assignment.save()
            return redirect('dashboard')

    return render_to_response('review/review_form.html', {'form':form, 'instance':review, 'assignment':assignment}, context_instance=RequestContext(request))
