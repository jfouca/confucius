from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods

from confucius.decorators import has_chair_role, has_role
from confucius.models import Alert, Conference, Membership, Paper, Assignment, Role


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
    from confucius.forms import MembershipForm

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
    form_class = modelform_factory(Conference, exclude=('members', 'is_open'))
    form = form_class(instance=request.conference)

    if 'POST' == request.method:
        form = form_class(request.POST, instance=request.conference)

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

    alerts_trigger = Alert.objects.filter(conference=conference.pk, reminder__isnull=True, action__isnull=True)
    alerts_reminder = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, action__isnull=True)
    alerts_action = Alert.objects.filter(conference=conference.pk, trigger_date__isnull=True, reminder__isnull=True)
    user_papers = Paper.objects.filter(conference=conference, submitter=request.user).order_by('-last_update_date')
    user_assignments = Assignment.objects.filter(reviewer=request.user, is_assigned=True)
    conference_reviews = Assignment.objects.filter(paper__conference=conference, is_done=True, review__isnull=False).order_by('-review__last_update_date')
    conference_papers = Paper.objects.filter(conference=conference).order_by('-submission_date')

    context = {
        'alerts_trigger': alerts_trigger,
        'alerts_reminder': alerts_reminder,
        'alerts_action': alerts_action,
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
def conference_invitation(request, template_name='conference/invitation.html'):
    pass


@require_http_methods(['GET', 'POST'])
@login_required
@has_chair_role
def conference_invite(request, template_name='conference/invitation_form.html'):
    from confucius.forms import InvitationForm
    from confucius.models import Invitation

    form = InvitationForm()

    if 'POST' == request.method:
        instance = Invitation(conference=request.conference)
        form = InvitationForm(request.POST, instance=instance)

        if form.is_valid():
            invitation = form.save(request)
            messages.success(request, u'An invitation has been sent to "%s".' % invitation.user)
            return redirect('dashboard')

    context = {
        'form': form,
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
