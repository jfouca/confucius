from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from confucius.forms import AddressFormSet, EmailFormSet, UserForm


@login_required
def edit_account(request):
    import json
    from django.http import HttpResponse

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        address_formset = AddressFormSet(request.POST, instance=request.user)
        email_formset = EmailFormSet(request.POST, instance=request.user)

        for f in (user_form, address_formset, email_formset):
            if f.is_valid():
                f.save()
            else:
                return HttpResponse(json.dumps(f.errors), content_type='text/plain')
    else:
        user_form = UserForm(instance=request.user)
        address_formset = AddressFormSet(instance=request.user)
        email_formset = EmailFormSet(instance=request.user)

    return render_to_response('account/edit_account.html',
        {'address_formset': address_formset, 'email_formset': email_formset, 'user_form': user_form},
        context_instance=RequestContext(request))


@login_required
def close_account(request):
    from django.contrib.auth import logout

    if request.method == 'POST':
        request.user.is_active = False
        request.user.save()
        logout(request)
        return HttpResponseRedirect(reverse('confirm_close_account'))
    return render_to_response('account/close_account.html', context_instance=RequestContext(request))


def confirm_close_account(request):
    return render_to_response('account/confirm_close_account.html', context_instance=RequestContext(request))
