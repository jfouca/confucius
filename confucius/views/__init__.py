<<<<<<< HEAD
from confucius.views.account import (close_account, edit_account, activate_account, create_account)
from confucius.views.conference import (ConferenceToggleView, ConferenceUpdateView, MembershipListView, create_alert, dashboard, reviewer_invitation, reviewer_response)
from confucius.views.submission import (submit_paper)
=======
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


class CsrfProtectView(FormView):
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CsrfProtectView, self).dispatch(*args, **kwargs)


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(*args, **kwargs)


class NeverCacheView(View):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(NeverCacheView, self).dispatch(*args, **kwargs)


from confucius.views.account import *
from confucius.views.conference import *
from confucius.views.submission import *
>>>>>>> 224597fc16a07cccf814e23c274d91138de40a88
from confucius.views.review import *
