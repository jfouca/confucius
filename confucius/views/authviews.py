from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Account
from confucius.forms import AccountForm


@login_required
def main_page(request):
    return render_to_response(
            'index.html',  context_instance=RequestContext(request))


@login_required
def edit_account(request):
    account = Account.objects.get(user=request.user)
    form = AccountForm(instance=account)
    return render_to_response('account/edit_account.html', {'form': form, 'account': account},
            context_instance=RequestContext(request))


def language_autocomplete(request):
    return HttpResponse("", content_type='text/plain')
