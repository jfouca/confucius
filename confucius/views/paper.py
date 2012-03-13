from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from confucius.decorators import has_submitter_role
from confucius.models import Paper


@require_http_methods(['GET', 'POST'])
@login_required
@has_submitter_role
@csrf_protect
def paper(request, paper_pk=None, template_name='conference/paper/paper_form.html'):
    from confucius.forms import PaperForm

    if not request.membership.has_chair_role() and not request.conference.is_open:
        messages.error(request,"The conference is closed.")
        return redirect('membership_list')
        
    if request.conference.has_finalize_paper_selections:
        messages.error(request,"The paper selection for this conference is now finished.")
        return redirect('dashboard', request.conference.pk)
        
        
    instance = Paper(**{'conference_id': request.conference.pk, 'submitter_id': request.user.pk})

    if paper_pk is not None:
        if request.membership.has_chair_role():
            instance = get_object_or_404(Paper, pk=paper_pk, conference=request.conference)
        else:
            instance = get_object_or_404(Paper, pk=paper_pk, conference=request.conference, submitter=request.user)

    form = PaperForm(instance=instance)

    if 'POST' == request.method:
        form = PaperForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, u'The paper "%s" has been successfully %s.' % (instance, 'submitted' if paper_pk is None else 'updated'))
            return redirect('papers', request.conference.pk)
        else:
            messages.error(request, u'Errors occured while %s the paper.'% ('submitting' if paper_pk is None else 'updating'))

    context = {
        'form': form,
        'conference': request.conference,
        'paper_pk': paper_pk
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))
