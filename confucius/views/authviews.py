from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.models import Account, EmailAddress, PostalAddress


@login_required
def main_page(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


@login_required
def edit_account(request):
    account = Account.objects.get(user=request.user)
    UserForm = modelform_factory(User, fields=('first_name', 'last_name',))
    AccountForm = modelform_factory(Account, exclude=('user','actual_conference'))
    EmailAddressFormSet = inlineformset_factory(Account, EmailAddress, extra=1)
    PostalAddressFormSet = inlineformset_factory(Account, PostalAddress, extra=1)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=account.user)
        account_form = AccountForm(request.POST, instance=account)
        emailaddress_set = EmailAddressFormSet(request.POST, instance=account)
        postaladdress_set = PostalAddressFormSet(request.POST, instance=account)

        for f in (user_form, account_form, emailaddress_set, postaladdress_set):
            if f.is_valid():
                f.save()
            else:
                return render_to_response('account/edit_account.html', {
        'userform': user_form, 'emailaddress_set': emailaddress_set,
        'postaladdress_set': postaladdress_set, 'account': account_form
        }, context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse('account'))
    else:
        user_form = UserForm(instance=account.user)
        account_form = AccountForm(instance=account)
        emailaddress_set = EmailAddressFormSet(instance=account)
        postaladdress_set = PostalAddressFormSet(instance=account)

    return render_to_response('account/edit_account.html', {
        'userform': user_form, 'emailaddress_set': emailaddress_set,
        'postaladdress_set': postaladdress_set, 'account': account_form
        }, context_instance=RequestContext(request))


@login_required
def close_account(request):
    from django.contrib.auth import logout
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        request.user.is_active = False
        request.user.save()
        logout(request)
        return render_to_response('account/confirm_close_account.html', {'account':account}, context_instance=RequestContext(request))
    return render_to_response('account/close_account.html', {'account':account}, context_instance=RequestContext(request))

