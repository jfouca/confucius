import simplejson
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext


from confucius.decorators import has_chair_role, has_reviewer_role
from confucius.forms import ReviewForm
from confucius.models import Assignment, Email, Membership, Paper, PaperSelection, Review, Role, User


@require_POST
@login_required
@has_chair_role
@csrf_protect
def auto_assignment(request):
    if request.is_ajax():
        start_time = time.time()*1000
    
        # Get datas
        conference = request.conference
        role = Role.objects.get(code="R")
        papers_list = Paper.objects.filter(conference=conference)
        papers_list = papers_list.annotate(domains_nb=Count('domains')).order_by("-domains_nb")
        max_assi_per_papers = request.POST.get('by_paper');
        max_assi_per_reviewers = request.POST.get('by_reviewer');
        
        if papers_list.count() <= 0 :
            return HttpResponse(status=403)
        
        
        # Clear assignments
        Assignment.objects.filter(conference=conference).delete()

        # Building an Assignment object from wrong informations. Will be manipulated (and avoid objects creations).
        assignment_object = Assignment.objects.create(paper=papers_list[0], reviewer=request.user, conference=conference)
        assignment_object.delete()      # Must delete to "clean" the object
        
        
        # Assignment per paper
        for paper in papers_list:
            assignment_object.paper = paper
            paper_domains = paper.domains.all()
            set_paper_domains = set(paper_domains)
            
            # Get reviewers (via memberships) who can be assigned for this paper
            memberships_list = Membership.objects.filter(conference=conference, roles=role, domains__in=paper_domains, user__languages=paper.language)
            memberships_list = memberships_list.annotate(assi_nb=Count('user__assignments')).annotate(domains_nb=Count('domains'))
            memberships_list = memberships_list.filter(assi_nb__lt=max_assi_per_reviewers).order_by("assi_nb", "domains_nb")
            
            
            # Reviewers, who have all the required skills for the paper, have the priority to be assigned.
            # Reviewers priority
            others_reviewers = []
            nb_assi = 0
            for membership in memberships_list:
                if paper.submitter == membership.user:
                    continue;
                    
                if nb_assi >= max_assi_per_papers:
                    break;
                    
                if set_paper_domains <= set(membership.domains.all()):
                    assignment_object.reviewer = membership.user
                    assignment_object.pk = None
                    assignment_object.save()
                    nb_assi += 1
                else:
                    others_reviewers.append(membership.user)           
            
            # Need more reviewers ? Use the "others" list !
            for reviewer in others_reviewers:
                if nb_assi >= max_assi_per_papers:
                    break;
                
                assignment_object.reviewer = reviewer
                assignment_object.pk = None
                assignment_object.save()
                nb_assi += 1
        
        
        end_time = time.time()*1000
        print str(end_time - start_time)
        
        
        # Response
        return HttpResponse(status=202)
        
        
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
@csrf_protect
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
        'memberships_list':memberships_list
    }
    
    return render_to_response('review/assignments.html', context, context_instance=RequestContext(request))

@require_POST
@login_required
@has_chair_role
@csrf_protect
def updateReviewerList(request):
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():
        conference = request.conference
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(pk=paper_id)
        
        role = Role.objects.get(name="Reviewer")
        memberships_list = Membership.objects.filter(roles=role,conference=conference).exclude(user__assignments__paper=paper)
        reviewers = [(membership.user.pk, membership.user.last_name+" "+membership.user.first_name+" ("+", ".join([domain.name for domain in membership.domains.all()])+") - ("+", ".join([language.name for language in membership.user.languages.all()])+")") for membership in memberships_list]
        
        data = simplejson.dumps(reviewers)
        return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)

@require_POST   
@login_required
@has_chair_role
@csrf_protect
def updateAssignmentsTables(request):      
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():     
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
        
        datas = [(assignment.pk, membership.user.pk, email.value, ", ".join([domain.name for domain in membership.domains.all()]), assignment.get_papers().count(), ", ".join([language.name for language in reviewer.languages.all()]) )]
        
        data = simplejson.dumps(datas)
        return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)

@require_POST
@login_required
@has_chair_role
@csrf_protect
def deleteAssignmentRow(request):
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():
        assignment_pk = request.POST.get('end')
        Assignment.objects.get(pk=assignment_pk).delete()
        return HttpResponse("Success")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)


@require_POST        
@login_required
@has_chair_role
@csrf_protect        
def refreshAssignationNumber(request):
    if request.is_ajax():
        conference = request.conference
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(pk=paper_id)
        assignments = paper.assignments.all()
        numbers = [( assignment.pk, assignment.get_papers().count()) for assignment in assignments]
        
        data = simplejson.dumps(numbers)
        return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)
        
