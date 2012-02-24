from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from confucius.models import Assignment, Review, Paper
from confucius.views import dashboard


@login_required
def auto_assignment(request, pk_paper):
    paper = Paper.objects.get(pk=pk_paper)
    
    assignment = Assignment.objects.create(reviewer=request.user, paper=paper)
    assignment.save()
    
    return redirect('dashboard')
