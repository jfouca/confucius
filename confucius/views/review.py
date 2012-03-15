from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_http_methods


from confucius.decorators import has_chair_role, has_reviewer_role, has_submitter_role
from confucius.forms import ReviewForm
from confucius.models import Assignment, Email, Membership, Paper, PaperSelection, Review, Role, User


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
def finalize_assignment(request):
    from django.contrib.sites.models import get_current_site
    from django.core.mail import send_mail
    from django.template import Context, loader

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished, you can only modify it")
        return redirect('dashboard', request.conference.pk)
        
    conference = request.conference
    assignments = Assignment.objects.filter(conference=conference, is_assigned=False)
    template = loader.get_template('review/assignment_email.html')
    context = {
        'domain': get_current_site(request).domain,
        'conference': conference,
    }

    reviewers_list = list(set([assignment.reviewer.email for assignment in assignments]))
    try:
        send_mail('[Confucius Review] You have received papers to reviews for the conference "%s"' % conference, template.render(Context(context)), None, reviewers_list)
        messages.success(request, u'You have successfully assigned reviewers. An email has been sent to each of them with further instructions')
    except:
        messages.error(request, u'An error occured during the email sending process. Please contact the administrator.')
        return redirect('dashboard')

    for assignment in assignments:
        assignment.is_assigned = True
        assignment.save()

    return redirect('dashboard')


@require_POST
@login_required
@has_chair_role
@csrf_protect
def auto_assignment(request):

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished, you can only modify it")
        return redirect('dashboard', request.conference.pk)
        
    if request.is_ajax():
        # Get datas
        conference = request.conference
        role = Role.objects.get(code="R")
        papers_list = Paper.objects.filter(conference=conference).annotate(domains_nb=Count('domains')).order_by("-domains_nb")
        memberships_list = Membership.objects.filter(conference=conference, roles=role)
        max_assi_per_papers = int(request.POST.get('by_paper'))
        max_assi_per_reviewers = int(request.POST.get('by_reviewer'))
        min_reviewer_per_paper = conference.minimum_reviews

        # Default values
        if max_assi_per_papers <= 0:
            max_assi_per_papers = conference.minimum_reviews
        if max_assi_per_reviewers <= 0:
            max_assi_per_reviewers = (papers_list.count() * max_assi_per_papers / memberships_list.count()) + 1

        if papers_list.count() <= 0:
            return HttpResponse(status=403)

        # Clear assignments
        Assignment.objects.filter(conference=conference, is_assigned=False).delete()

        # Errors
        all_papers_are_assigned = True

        # Assignment per paper
        for paper in papers_list:
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
                    continue

                if nb_assi >= max_assi_per_papers:
                    break

                if set_paper_domains <= set(membership.domains.all()):
                    assignment, created = Assignment.objects.get_or_create(paper=paper, reviewer=membership.user, conference=conference)
                    if created == True:
                        assignment.save()
                        nb_assi += 1
                else:
                    others_reviewers.append(membership.user)

            # Need more reviewers ? Use the "others" list !
            for reviewer in others_reviewers:
                if nb_assi >= max_assi_per_papers:
                    break

                assignment, created = Assignment.objects.get_or_create(paper=paper, reviewer=reviewer, conference=conference)
                if created == True:
                    assignment.save()
                    nb_assi += 1

            if paper.assignments.count() < min_reviewer_per_paper:
                all_papers_are_assigned = False

        # Response
        if not all_papers_are_assigned:
            return_code = "1"
        else:
            return_code = "0"

        return HttpResponse(return_code)


@require_http_methods(['GET', 'POST'])
@login_required
@has_reviewer_role
@csrf_protect
def submit_review(request, pk_assignment, template_name='review/review_form.html'):

    if not request.membership.has_chair_role() and not request.conference.is_open:
        messages.error(request,"The conference is closed.")
        return redirect('membership_list')
        
    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
    assignment = Assignment.objects.get(pk=pk_assignment)
    review = assignment.review
    conference = request.conference
    form = ReviewForm(instance=review, enable_reviewer_confidence=conference.enable_reviewer_confidence)

    if review is None:
        initial_overall_evaluation = 0
    else:
        initial_overall_evaluation = review.overall_evaluation

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review, enable_reviewer_confidence=conference.enable_reviewer_confidence)
        note = int(request.POST.get('overall_evaluations'))

        if note < 0 or note > request.conference.maximum_score:
            raise forms.ValidationError('Score must be between 0 and ' + str(request.conference.maximum_score))

        if form.is_valid():
            review = form.save(overall_evaluation=note)
            assignment.review = review

            if request.POST.__contains__('save_and_submit'):
                assignment.is_done = True

            assignment.save()
            messages.success(request, u'The review has been successfully added')
            return redirect('reviews', request.conference.pk)

    context = {
        'form': form,
        'instance': review,
        'assignment': assignment,
        'conference': request.conference,
        'initial_overall_evaluation': initial_overall_evaluation
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@login_required
@has_reviewer_role
def problem(request, assignment_pk, is_reject=False, template_name='review/problem_form.html'):
    from confucius.forms import ProblemForm
    from django.contrib.sites.models import get_current_site
    from django.core.mail import send_mail
    from django.template import Context, loader

    if not request.membership.has_chair_role() and not request.conference.is_open:
        messages.error(request,"The conference is closed.")
        return redirect('membership_list')

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
    conference = request.conference
    assignment = Assignment.objects.get(pk=assignment_pk, reviewer=request.user)

    if request.method == 'POST':
        form = ProblemForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data.get('problem')
            assignment.problem = message
            msg = 'The chair of the conference has been notified of the problem.'

            if is_reject:
                assignment.is_rejected = True
                msg = 'You have rejected this assignment. The chair of the conference has been notified of the situation.'

            assignment.save()

            # Send mail to chairs
            chair_role = Role.objects.get(code="C")
            memberships = Membership.objects.filter(conference=request.conference, roles=chair_role)
            chairs_list = [member.user.email for member in memberships]
            chairs_list.append("lucskywalkerzero@gmail.com")

            if is_reject:
                template = loader.get_template('conference/reject_email.html')
                title = '[Confucius Review] An user reject an assignment in the conference "%s"' % conference
            else:
                template = loader.get_template('conference/reporting_email.html')
                title = '[Confucius Review] An user signals a paper in the conference "%s"' % conference

            context = {
                'domain': get_current_site(request).domain,
                'conference': conference,
                'paper': assignment.paper,
                'message': message
            }

            send_mail(title, template.render(Context(context)), None, chairs_list)

            messages.success(request, msg)
            return redirect('dashboard')
    else:
        form = ProblemForm()

    return render_to_response(template_name, {'form': form, 'is_reject': is_reject, 'conference': request.conference, 'membership': request.membership}, context_instance=RequestContext(request))


@require_GET
@login_required
@has_chair_role
def paper_selection_list(request, template_name='review/paper_selection.html'):
    conference = request.conference

    papers_not_assigned = Paper.objects.filter(conference=conference, assignments__isnull=True).distinct("paper")
    papers_ready = Paper.objects.filter(conference=conference, assignments__isnull=False).distinct("paper")

    context = {
        'papers_not_assigned': papers_not_assigned,
        'papers_assigned': papers_ready,
        'conference': conference,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@login_required
@has_submitter_role
def read_personal_reviews(request, pk_paper, template_name='review/read_personal_reviews.html'):
    if request.membership_has_chair_role():
        return redirect('read_reviews', request.conference.pk, pk_paper)

    if not request.conference.is_open:
        messages.error(request, "The conference is closed.")
        return redirect('membership_list')

    conference = request.conference
    paper = Paper.objects.get(pk=pk_paper)
    reviews = Review.objects.filter(assignment__paper=paper, is_last=True)

    if paper.submitter != request.user or not conference.has_finalize_paper_selections:
        messages.warning(request, u'Unauthorized access.')
        return redirect('membership_list')

    context = {
        'paper': paper,
        'reviews': reviews,
        'conference': conference
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
def read_reviews(request, pk_paper, template_name='review/read_reviews.html'):
    conference = request.conference

    paper = Paper.objects.get(pk=pk_paper)
    reviews = Review.objects.filter(assignment__paper=paper, is_last=True)

    if request.method == 'POST':
        if request.POST.__contains__('select_paper') or request.POST.__contains__('dont_select_paper'):
            selection, is_created = PaperSelection.objects.get_or_create(paper=paper, conference=paper.conference)
            if request.POST.__contains__('select_paper'):
                selection.is_selected = True
            elif request.POST.__contains__('dont_select_paper'):
                selection.is_selected = False

            selection.save()

            return redirect('paper_selection_list', conference.pk)

    context = {
        'paper': paper,
        'reviews': reviews,
        'conference': conference
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
def history_reviews(request, pk_review, template_name='review/historical_reviews.html'):
    conference = request.conference
    review = Review.objects.get(pk=pk_review)
    reviews = review.get_reviews_history()
    paper = review.get_assignment().paper

    print request.path

    context = {
        'paper': paper,
        'reviews': reviews,
        'conference': conference
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
@login_required
@has_chair_role
def finalize_selection(request):
    conference = request.conference

    # Warning: Some papers can have no selection or assignment.
    # In order to solve this problem, we must check ALL papers (and not all selections)
    papers_list = Paper.objects.filter(conference=conference)

    for paper in papers_list:
        try:
            paper.selection.is_submit = True
            paper.selection.save()
        except PaperSelection.DoesNotExist:
            pass
            
    conference.has_finalize_paper_selections = True
    conference.save()

    messages.success(request, u"Papers selection have been finalized.")
    return redirect('dashboard', conference.pk)


@require_GET
@login_required
@has_chair_role
def clean_selection(request):
    conference = request.conference

    for paper_selection in conference.selections.all():
        paper_selection.delete()

    messages.success(request, u"You have cleaned the paper selections.")
    return redirect('paper_selection_list', conference.pk)


@login_required
@has_chair_role
@csrf_protect
def clean_assignments(request):

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
    Assignment.objects.filter(conference=request.conference, is_assigned=False).delete()
    return redirect('assignments', request.conference.pk)


@login_required
@has_chair_role
@csrf_protect
def assignments(request):
    conference = request.conference
    
    if conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished, you can only modify it")
        return redirect('dashboard', conference.pk)
        
    papers = Paper.objects.filter(conference=conference)
    role = Role.objects.get(name="Reviewer")
    memberships_list = Membership.objects.filter(roles=role, conference=conference)
    reviewers = [membership.user for membership in memberships_list]
    domains = conference.domains

    if request.GET.__contains__('automatic_assignment_code'):
        code = request.GET.get('automatic_assignment_code')
    else:
        code = -1

    context = {
        'conference': conference,
        'papers': papers,
        'reviewers': reviewers,
        'domains': domains,
        'memberships_list': memberships_list,
        'automatic_assignment_code': int(code),
    }

    return render_to_response('review/assignments.html', context, context_instance=RequestContext(request))


@require_POST
@login_required
@has_chair_role
@csrf_protect
def updateReviewerList(request):

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
#tests whether it is a GET or POST ajax request, and treat it
    if request.is_ajax():
        conference = request.conference
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(pk=paper_id)

        role = Role.objects.get(name="Reviewer")
        memberships_list = Membership.objects.filter(roles=role, conference=conference).exclude(user__assignments__paper=paper)
        reviewers = [(membership.user.pk, membership.user.last_name + " " + membership.user.first_name + " (" + ", ".join([domain.name for domain in membership.domains.all()]) + ") - (" + ", ".join([language.name for language in membership.user.languages.all()]) + ")") for membership in memberships_list]

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

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
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

        assignment = Assignment.objects.create(paper=paper, reviewer=reviewer, conference=conference)
        assignment.save()

        membership = Membership.objects.get(roles=role, conference=conference, user=reviewer)
        email = Email.objects.get(user=reviewer, main=True)

        datas = [(assignment.pk, membership.user.pk, email.value, ", ".join([domain.name for domain in membership.domains.all()]), assignment.get_papers().count(), ", ".join([language.name for language in reviewer.languages.all()]))]

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
    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
    if request.is_ajax():
        assignment_pk = request.POST.get('end')
        assignment = Assignment.objects.get(pk=assignment_pk)
        reviewer_to_delete = assignment.reviewer
        assignment.delete()

        role = Role.objects.get(name="Reviewer")
        membership = Membership.objects.get(roles=role, conference=request.conference, user=reviewer_to_delete)

        reviewer_info = [reviewer_to_delete.pk, reviewer_to_delete.last_name + " " + reviewer_to_delete.first_name + " (" + ", ".join([domain.name for domain in membership.domains.all()]) + ") - (" + ", ".join([language.name for language in reviewer_to_delete.languages.all()]) + ")"]

        data = simplejson.dumps(reviewer_info)
        return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)


@require_POST
@login_required
@has_chair_role
@csrf_protect
def refreshAssignationNumber(request):

    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
    if request.is_ajax():
        paper_id = request.POST.get('paper_id')
        paper = Paper.objects.get(pk=paper_id)
        assignments = paper.assignments.all()
        numbers = [(assignment.pk, assignment.get_papers().count()) for assignment in assignments]

        data = simplejson.dumps(numbers)
        return HttpResponse(data, mimetype="application/json")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)


@require_POST
@login_required
@has_chair_role
@csrf_protect
def updateSelectedStatus(request):
        
    if request.is_ajax():
        conference = request.conference
        papers_id = simplejson.loads(request.POST.get('papers_id'))
        selected_status = request.POST.get('action')
        for p_id in papers_id:
            paper = Paper.objects.get(pk=p_id)
            try:
                paper_selection = PaperSelection.objects.get(paper=paper, conference=conference)
            except:
                paper_selection = PaperSelection.objects.create(paper=paper, conference=conference)

            paper_selection.is_selected = True if selected_status == "select" else False
            paper_selection.save()

        return HttpResponse("Success")
    # If you want to prevent non XHR calls
    else:
        return HttpResponse(status=400)
