from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import modelform_factory, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Account, Language, EmailAddress, PostalAddress


@login_required
def main_page(request):
    return render_to_response(
        'index.html',  context_instance=RequestContext(request))


@login_required
def edit_account(request):
    account = Account.objects.get(user=request.user)
    UserForm = modelform_factory(User, fields=('first_name', 'last_name',))
    AccountForm = modelform_factory(Account, exclude=('user',))
    EmailAddressFormSet = inlineformset_factory(Account, EmailAddress, extra=0)

    if request.POST:
        user_form = UserForm(request.POST, instance=account.user)
        account_form = AccountForm(request.POST, instance=account)
        emailaddress_set = EmailAddressFormSet(request.POST, instance=account)

        for f in (user_form, account_form, emailaddress_set):
            if f.is_valid():
                f.save()
    else:
        user_form = UserForm(instance=account.user)
        account_form = AccountForm(instance=account)
        emailaddress_set = EmailAddressFormSet(instance=account)

    return render_to_response('account/edit_account.html', {
        'user': user_form, 'emailaddress_set': emailaddress_set,
        'account': account_form},
        context_instance=RequestContext(request))


def language_autocomplete(request):
    return HttpResponse("", content_type='text/plain')
