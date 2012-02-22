from django.conf import settings
from django.contrib.auth.views import redirect_to_login


class LoginRequiredMiddleware(object):
    def process_request(self, request):
        if (not request.user.is_authenticated() and
            not request.get_full_path().startswith(settings.LOGIN_URL)):
            return redirect_to_login(request.get_full_path())
