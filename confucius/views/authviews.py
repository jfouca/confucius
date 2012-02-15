from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Profile
from confucius.forms import ProfileForm


@login_required
def edit_profile(request):
    p = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=p)
    return render_to_response('registration/edit_profile.html', {'form': form},
            context_instance=RequestContext(request))
