from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import DetailView

from confucius.forms import AddressFormSet, EmailFormSet, UserForm
from confucius.models import Activation
from confucius.views import NeverCacheView


class ConfirmEmailView(NeverCacheView, DetailView):
    context_object_name = 'email'
    template_name = 'registration/email_confirm.html'

    def get_object(self):
        activation_key = self.kwargs.get('activation_key', None)

        try:
            activation = Activation.objects.get(activation_key=activation_key)
            activation.delete()
        except Activation.DoesNotExist:
            return None

        if activation.has_expired():
            return None

        activation.email.confirmed = True
        activation.email.save()

        return activation.email


@login_required
def edit_account(request, template='account/edit_account.html'):
    import json
    from django.http import HttpResponse
    from confucius.utils import errors_to_dict

    form = UserForm(instance=request.user)
    address_formset = AddressFormSet(instance=request.user)
    email_formset = EmailFormSet(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        address_formset = AddressFormSet(request.POST, instance=request.user)
        email_formset = EmailFormSet(request.POST, instance=request.user)
        errors = {}

        for f in (form, address_formset, email_formset):
            if f.is_valid():
                f.save()
            else:
                errors = dict(errors.items() + errors_to_dict(f).items())

        return HttpResponse(json.dumps(errors), content_type='text/plain')

    context = {
        'address_formset': address_formset,
        'email_formset': email_formset,
        'form': form
    }

    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def close_account(request):
    from django.contrib.auth import logout
    from django.contrib import messages

    request.user.is_active = False
    request.user.save()
    logout(request)
    messages.info(request, 'Your account has been closed.')
    return redirect('login')
