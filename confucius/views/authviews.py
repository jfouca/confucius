from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.forms import ProfileForm
from confucius.models import Profile


@login_required
def edit_profile(request, form_class=ProfileForm,
    template_name='registration/edit_profile.html'):

    profile = None

    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
    else:
        form = form_class(instance=profile)

    context = RequestContext(request)

    return render_to_response(template_name,
        {'form': form, 'profile': profile}, context_instance=context)
