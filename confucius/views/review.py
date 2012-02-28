import simplejson

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from confucius.decorators import has_chair_role, has_reviewer_role
from confucius.forms import ReviewForm
from confucius.models import Assignment, Email, Membership, Paper, PaperSelection, Review, Role, User
import time

@require_POST
@login_required
@has_chair_role
@csrf_protect
def auto_assignment(request):
    if request.is_ajax():
        #to show the modal frame in assignments.html
        time.sleep(4)
        
        
        conference = request.conference

        role = Role.objects.get(code="R")
        papers_list = Paper.objects.filter(conference=conference)
        memberships_list = Membership.objects.filter(conference=conference, roles=role)
       
       
        if memberships_list.count() <= 0 or papers_list.count() <= 0 :
            return HttpResponse("Fail")
       
        # Clear assignments
        Assignment.objects.filter(paper__conference=conference).delete()
       
       
        # Assignments
        for paper in papers_list:
           paper_domains = paper.domains.all()
           paper_language = paper.language
          
           #results = memberships_list.filter(domains__in=paper_domains, user__languages=paper_language)
           results = memberships_list.filter(domains=paper_domains)
           if results.count() > 0:
                results = results.distinct("user")
               
                for result in results:
                    user = result.user
                    Assignment.objects.create(paper=paper, reviewer=user, conference=conference).save()
       
       
        # Check assignments load
        assignments = Assignment.objects.filter(paper__conference=conference)
        nb_assignments = assignments.count()
        avg_assi_by_papers = (nb_assignments / papers_list.count())
        avg_assi_by_reviewers = (nb_assignments / memberships_list.count())
       
        avg_assi_by_papers = 3
        avg_assi_by_reviewers = 3
       
        memberships = memberships_list.annotate(assi_nmb=Count('user__assignments')).filter(assi_nmb__gt=avg_assi_by_reviewers).order_by("-assi_nmb")
       
        for membership in memberships:
            user = membership.user
            nb_assignments_to_remove = membership.assi_nmb - avg_assi_by_reviewers
           
            print user, nb_assignments_to_remove
           
            #assignments = Assignment.objects.filter(paper__conference=conference).annotate(paper_nmb=Count('paper__assignments')).filter(reviewer=user, paper_nmb__gt=avg_assi_by_papers)
            assignments = Assignment.objects.filter(paper__conference=conference).annotate(paper_nmb=Count('paper__assignments')).filter(reviewer=user, paper_nmb__gt=avg_assi_by_papers)
            if assignments.count() < nb_assignments_to_remove:
                nb_assignments_to_remove = assignments.count()
           
            print user, nb_assignments_to_remove
            for assignment in assignments[:nb_assignments_to_remove]:
                assignment.delete()
               
       
        # Response
        return HttpResponse("Success")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)
    
        
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

@login_required
@has_chair_role
def assignments(request):
    conference = request.conference
    papers = Paper.objects.filter(conference=conference)
    role = Role.objects.get(name="Reviewer")
    memberships_list = Membership.objects.filter(roles=role,conference=conference)
    reviewers = [membership.user for membership in memberships_list]
    domains = conference.domains
    
    context = {
        'conference':conference,
        'papers':papers,
        'reviewers':reviewers,
        'domains':domains,
    }
    return render_to_response('review/assignments.html', context, context_instance=RequestContext(request))


@login_required
@has_chair_role
@csrf_protect
def updateReviewerList(request):
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():
        if request.method == 'POST':
            conference = request.conference
            paper_id = request.POST.get('paper_id')
            paper = Paper.objects.get(pk=paper_id)
            
            role = Role.objects.get(name="Reviewer")
            memberships_list = Membership.objects.filter(roles=role,conference=conference).exclude(user__assignments__paper=paper)
            reviewers = [(membership.user.pk, membership.user.last_name+" "+membership.user.first_name+" ("+", ".join([domain.name for domain in membership.domains.all()])+")") for membership in memberships_list]
            
            data = simplejson.dumps(reviewers)
            return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)
        
@login_required
@has_chair_role
@csrf_protect
def updateAssignmentsTables(request):      
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():     
        if request.method == 'POST':
            conference = request.conference
            paper_id = request.POST.get('paper_id')
            reviewer_id = request.POST.get('reviewer_id')
            
            reviewer = User.objects.get(pk=reviewer_id)
            paper = Paper.objects.get(pk=paper_id)
            role = Role.objects.get(name="Reviewer")
            membership = Membership.objects.get(roles=role, user=reviewer, conference=conference)                 
            conference = membership.conference
            
                        
            assignment = Assignment.objects.create(paper=paper,reviewer=reviewer, conference=conference)
            assignment.save()
            
            membership = Membership.objects.get(roles=role,conference=conference,user=reviewer)
            email = Email.objects.get(user=reviewer,main=True)
            
            datas = [(assignment.pk, membership.user.pk, email.value, ", ".join([domain.name for domain in membership.domains.all()]), assignment.get_papers().count())]
            
            data = simplejson.dumps(datas)
            return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)

@login_required
@has_chair_role
@csrf_protect
def deleteAssignmentRow(request):
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():
        if request.method == 'POST':
            assignment_pk = request.POST.get('end')
            Assignment.objects.get(pk=assignment_pk).delete()
            return HttpResponse("kikou")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)
