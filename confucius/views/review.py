from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from confucius.decorators import has_chair_role, has_reviewer_role
from confucius.forms import ReviewForm
from confucius.models import Assignment, Membership, Paper, PaperSelection, Review


@require_POST
@login_required
@has_chair_role
def auto_assignment(request, pk_paper):
    paper = Paper.objects.get(pk=pk_paper)

    assignment = Assignment.objects.create(reviewer=request.user, paper=paper)
    assignment.save()

    return redirect('dashboard')


@require_http_methods(['GET', 'POST'])
@login_required
@has_reviewer_role
@csrf_protect
def submit_review(request, pk_assignment, template_name='review/review_form.html'):
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

    context = {
        'form': form,
        'instance': review,
        'assignment': assignment,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
@login_required
@has_chair_role
def paper_selection_list(request, template_name='review/paper_selection_list.html'):
    conference = request.conference

    papers_not_assigned = Paper.objects.filter(conference=conference, assignments__isnull=True)
    assignments_without_reviews = Assignment.objects.filter(paper__conference=conference, is_done=False)
    papers_ready = Paper.objects.filter(conference=conference, assignments__is_done=True)

    context = {
        'papers_not_assigned': papers_not_assigned,
        'assignments_without_reviews': assignments_without_reviews,
        'papers_ready': papers_ready,
        'conference': conference,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
def read_reviews(request, pk_paper, template_name='review/read_reviews.html'):
    paper = Paper.objects.get(pk=pk_paper)
    reviews = Review.objects.filter(assignment__paper=paper)

    if request.method == 'POST':
        if request.POST.__contains__('select_paper') or request.POST.__contains__('dont_select_paper'):
            selection, is_created = PaperSelection.objects.get_or_create(paper=paper, conference=paper.conference)
            if request.POST.__contains__('select_paper'):
                selection.is_selected = True
            elif request.POST.__contains__('dont_select_paper'):
                selection.is_selected = False

            selection.save()

            return redirect('paper_selection_list')

    context = {
        'paper': paper,
        'reviews': reviews,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
@login_required
@has_chair_role
def finalize_selection(request):
    membership = Membership.objects.get(user=request.user, last_accessed=True)
    conference = membership.conference

    for paper_selection in conference.selections.all():
        paper_selection.is_submit = True
        paper_selection.save()

    conference.has_finalize_paper_selections = True
    conference.save()

    return redirect('dashboard')
