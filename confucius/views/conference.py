from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods

from confucius.decorators import has_chair_role, has_role, has_reviewer_role, has_submitter_role
from confucius.forms import ConferenceForm, MembershipForm, SendEmailToUsersForm
from confucius.models import Alert, Assignment, Conference, Invitation, Membership, Paper, PaperSelection, Role, User
from confucius.utils import send_emails_to_group

@require_GET
def conference_access(request, conference_pk, access_key, template_name='conference/membership_form.html'):
    conference = get_object_or_404(Conference, pk=conference_pk, access_key=access_key)

    if request.user.is_authenticated():
        try:
            Membership.objects.get(user=request.user, conference=conference)
            return redirect('dashboard', conference_pk=conference_pk)
        except:
            pass

        return redirect('membership', conference_pk=conference_pk)
    else:
        # We don't handle anonymous users, yet.
        return redirect('login')


@require_http_methods(['GET', 'POST'])
@login_required
@csrf_protect
def membership(request, conference_pk, template_name='conference/membership_form.html'):
    conference = Conference.objects.get(pk=conference_pk)

    try:
        membership = Membership.objects.get(user=request.user, conference=conference)
    except:
        membership = Membership(**{'conference': conference, 'user': request.user})

    form = MembershipForm(instance=membership)

    if 'POST' == request.method:
        form = MembershipForm(request.POST, instance=membership)

        if form.is_valid():
            membership = form.save()
            membership.roles.add(Role.objects.get(code='S'))
            messages.success(request, u'Your membership has been sucessfully updated.')
            return redirect('dashboard', conference_pk=membership.conference.pk)

    context = {
        'form': form,
        'conference': conference,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
@csrf_protect
def conference_edit(request, template_name='conference/conference_form.html'):
    form = ConferenceForm(instance=request.conference)

    if 'POST' == request.method:
        form = ConferenceForm(request.POST, instance=request.conference)

        if form.is_valid():
            request.conference = form.save()
            messages.success(request, u'The conference "%s" has been successfully updated.' % request.conference)
            return redirect('dashboard')

    context = {
        'conference': request.conference,
        'form': form,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
@login_required
@has_chair_role
def conference_toggle(request):
    conference = request.conference
    conference.is_open = not conference.is_open
    conference.save()
    messages.success(request, u'You have %s the conference %s' % ('opened' if conference.is_open else 'closed', conference.title))
    return redirect(request.META.get('HTTP_REFERER', 'membership_list'))


@require_GET
@login_required
@has_role
def dashboard(request, template_name='conference/dashboard.html'):
    from django.contrib.sites.models import get_current_site

    conference = request.conference
    membership = request.membership

    user_papers = Paper.objects.filter(conference=conference, submitter=request.user).order_by('-last_update_date')
    user_assignments = Assignment.objects.filter(conference=conference, reviewer=request.user, is_assigned=True)
    
    
    alerts_trigger = Alert.objects.filter(conference=conference.pk, reminder__isnull=True, action__isnull=True).order_by('trigger_date')
    #alerts_reminder = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, action__isnull=True)
    #alerts_action = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, reminder__isnull=True)
    if alerts_trigger.count() > 5:
        alerts_trigger = alerts_trigger[:5]
    
    conference_reviews = Assignment.objects.filter(paper__conference=conference, is_done=True, review__isnull=False).order_by('-review__last_update_date')
    if conference_reviews.count() > 5:
        conference_reviews = conference_reviews[:5]
        
    conference_papers = Paper.objects.filter(conference=conference).order_by('-submission_date')
    if conference_papers.count() > 5:
        conference_papers = conference_papers[:5]

    context = {
        'alerts_trigger': alerts_trigger,
        'conference': conference,
        'membership': membership,
        'user_papers': user_papers,
        'conference_papers': conference_papers,
        'user_assignments': user_assignments,
        'conference_reviews': conference_reviews,
        'public_url': 'http://%s%s' % (get_current_site(request).domain, conference.get_absolute_url())
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
def conference_invitation(request, key, decision, template_name='conference/invitation.html'):
    invitation = get_object_or_404(Invitation, key=key)

    if not invitation.pending():
        return redirect('already_answered')

    if decision == 'refuse':
        invitation.refuse()
        return redirect('refusal')

    if not invitation.user.is_active:
        return redirect('signup', key=key)

    invitation.accept()

    try:
        membership = Membership.objects.get(user=invitation.user, conference=invitation.conference)
    except:
        membership = Membership.objects.create(user=invitation.user, conference=invitation.conference)

    membership.roles.clear()
    for role in invitation.roles.all():
                membership.roles.add(role)
    membership.save()

    messages.success(request, u'You are now participating in the conference "%s"' % invitation.conference)
    return redirect('dashboard', conference_pk=invitation.conference.pk)


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
def conference_invite(request, template_name='conference/invitation_form.html'):
    from confucius.forms import InvitationForm

    form = InvitationForm()

    if 'POST' == request.method:
        instance = Invitation(conference=request.conference)
        form = InvitationForm(request.POST, instance=instance)

        if form.is_valid():
            try:
                invitation = form.save(request)
                messages.success(request, u'An invitation has been sent to "%s".' % invitation.user)
            except:
                user = User.objects.get(email=form.cleaned_data['email']).delete()
                messages.error(request, u'An error occured during the email sending process. Please contact the administrator.')
            return redirect('invitations', request.conference.pk)

    context = {
        'form': form,
        'conference': request.conference,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
@login_required
def membership_list(request, template_name='conference/membership_list.html'):
    membership_list = Membership.objects.filter(user=request.user)

    context = {
        'membership_list': membership_list,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST'])
@csrf_protect
def signup(request, key, template_name='registration/signup_form.html'):
    from django.contrib.auth import authenticate, login
    from django.db.models import Q
    from confucius.forms import PaperForm, SignupForm

    if request.user.is_authenticated():  # You're already registered, what the fuck would you signup for?
        return redirect('dashboard')

    invitation = get_object_or_404(Invitation, key=key)

    try:
        invitation.roles.filter(Q(code='R') | Q(code='C'))
        instance = Membership(**{'conference': invitation.conference, 'user': invitation.user})
        extra_form_class = MembershipForm
    except:
        instance = Paper(**{'conference': invitation.conference, 'submitter': invitation.user})
        extra_form_class = PaperForm

    form = SignupForm(instance=invitation.user)
    extra_form = extra_form_class(instance=instance)

    if request.method == 'POST':
        form = SignupForm(request.POST, instance=invitation.user)
        extra_form = extra_form_class(request.POST, request.FILES, instance=instance)

        for f in (form, extra_form):
            if f.is_valid():
                f.save()

        if not form.errors and not extra_form.errors:
            invitation.accept()
            user = authenticate(username=invitation.user.email, password=form.cleaned_data.get('password1'))
            login(request, user)
            # Add roles
            membership = Membership.objects.get(user=invitation.user, conference=invitation.conference)

            for role in invitation.roles.all():
                membership.roles.add(role)
            membership.save()
            messages.success(request, u'Congratulations! Welcome to the conference.')
            return redirect('dashboard', invitation.conference.pk)

    context = {
        'form': form,
        'extra_form': extra_form,
        'invitation': invitation,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@has_chair_role
@csrf_protect
def send_email_to_users(request, template_name='conference/send_email_to_users.html'):

    conference = request.conference
    form = SendEmailToUsersForm(initial={'conference': conference})

    if 'POST' == request.method:
        form = SendEmailToUsersForm(request.POST, initial={'conference': conference})

        if form.is_valid():
            #Get the cleaned_data from FORM and then send the email
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            if len(form.cleaned_data['users']) > 0 :
                receivers = form.cleaned_data['users']
                send_emails_to_group(receivers, title, content, request)
            else:
                groups = form.cleaned_data['groups']
                if "U" in groups:
                    receivers = [paperselect.paper.submitter for paperselect in PaperSelection.objects.filter(conference=conference) if paperselect.is_selected and paperselect.is_submit]
                    send_emails_to_group(receivers, title, content, request)
                    
                roles = groups.remove("U")
                if roles is not None:
                    for role in roles:
                        memberships_list = Membership.objects.filter(roles=role, conference=conference)
                        receivers = [membership.user for membership in memberships_list]                   
                        send_emails_to_group(receivers, title, content, request)
            
    context = {
        'form': form,
        'conference': conference
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@has_submitter_role
def paper_list(request, get_all=False, template_name='conference/paper_list.html'):
    conference = request.conference

    if get_all == False:
        papers = Paper.objects.filter(conference=conference, submitter=request.user)
    else:    
        papers = Paper.objects.filter(conference=conference)
        
    context = {
        'paper_list': papers,
        'conference': conference,
        'membership': request.membership,
        'is_conference_papers': get_all
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@has_reviewer_role
def review_list(request, get_all=False, template_name='conference/review_list.html'):
    conference = request.conference

    if get_all == False:
        user_assignments = Assignment.objects.filter(conference=conference, reviewer=request.user, is_assigned=True)
    else:
        user_assignments = Assignment.objects.filter(conference=conference, is_assigned=True)
    
    context = {
        'user_assignments': user_assignments,
        'conference': conference,
        'membership': request.membership,
        'is_conference_reviews': get_all
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@has_chair_role
def alert_list(request, template_name='conference/alert_list.html'):
    conference = request.conference

    alerts_trigger = Alert.objects.filter(conference=request.conference, reminder__isnull=True, action__isnull=True)
    alerts_reminder = Alert.objects.filter(conference=request.conference, trigger_date__isnull=True, action__isnull=True)
    alerts_action = Alert.objects.filter(conference=request.conference, trigger_date__isnull=True, reminder__isnull=True)

    context = {
        'alerts_trigger': alerts_trigger,
        'alerts_reminder': alerts_reminder,
        'alerts_action': alerts_action,
        'conference': conference,
        'membership': request.membership
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@has_chair_role
def invitation_list(request, template_name='conference/invitation_list.html'):
    conference = request.conference

    invitations = Invitation.objects.filter(conference=conference)

    context = {
        'invitation_list': invitations,
        'conference': conference,
        'membership': request.membership
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))
    
    
@login_required
@has_chair_role
def members_list(request, template_name='conference/members_list.html'):
    conference = request.conference

    role = Role.objects.get(name="Reviewer")
    memberships_list = Membership.objects.filter(roles=role, conference=conference)
    reviewers = [[membership.user, membership.domains] for membership in memberships_list]
    
    role = Role.objects.get(name="Submitter")
    memberships_list = Membership.objects.filter(roles=role, conference=conference)
    submitters = [[membership.user, membership.domains] for membership in memberships_list]
    
    role = Role.objects.get(name="Chair")
    memberships_list = Membership.objects.filter(roles=role, conference=conference)
    chairs = [[membership.user, membership.domains] for membership in memberships_list]
    
    context = {
        'conference': conference,
        'chairs': chairs,
        'reviewers': reviewers,
        'submitters': submitters
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))
