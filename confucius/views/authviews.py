from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

from django.http import HttpResponse


@login_required
def profile(request):
    return HttpResponse(request.user.username)
