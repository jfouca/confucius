from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods


@require_http_methods(['GET', 'POST'])
@login_required
@csrf_protect
def account(request, template='account/account_form.html'):
    """
    Basic detail/edit view.
    """
    from confucius.forms import AddressFormSet, EmailFormSet, UserForm

    form = UserForm(instance=request.user)
    address_formset = AddressFormSet(instance=request.user)
    email_formset = EmailFormSet(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        address_formset = AddressFormSet(request.POST, instance=request.user)
        email_formset = EmailFormSet(request.POST, instance=request.user)
        error = False

        for f in (form, address_formset, email_formset):
            if f.is_valid():
                f.save()
            else:
                error = True

        if not error:
            return redirect('account')

    context = {
        'address_formset': address_formset,
        'email_formset': email_formset,
        'form': form
    }

    return render_to_response(template, context, context_instance=RequestContext(request))


@require_GET
@login_required
def close_account(request):
    """
    The User is not deleted, just deactivated.
    """
    from django.contrib.auth import logout

    if request.user.is_superuser:
        messages.error(request, u"Since you're a superuser, you can't lock yourself out by closing your own account.")
        return redirect('account')

    request.user.is_active = False
    request.user.save()
    logout(request)
    messages.info(request, u'Your account has been successfully closed.')
    return redirect('login')


@require_GET
def confirm_email(request, activation_key):
    """
    This is where the User lands when he follows the link sent to him via email
    No need for login_required since the User can be new (and therefore can't log in, yet),
    plus the activation_key is unpredictable.
    """
    from confucius.models import Activation

    try:
        activation = Activation.objects.get(activation_key=activation_key)
    except Activation.DoesNotExist:
        activation = None

    if activation is not None:
        email = activation.email
        email.confirmed = True
        email.save()
        if email.main:
            email.user.is_active = True
            email.user.save()
        activation.delete()
        messages.success(request, 'The email "%s" has been confirmed.' % email)
    else:
        messages.error(request, 'The activation key used is invalid or has expired.')

    return redirect('account')


@require_http_methods(['GET', 'POST'])
@login_required
@csrf_protect
def password_change(request, template_name='account/password_change_form.html'):
    """
    Overridden to make use of django's messages framework
    """
    from django.contrib.auth.forms import PasswordChangeForm

    form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, u'Your password has been successfully updated.')
            return redirect('account')

    context = {
        'form': form,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@require_GET
@login_required
def languages(request):
    import json
    from django.http import HttpResponse
    from confucius.models import Language

    return HttpResponse(json.dumps([unicode(l) for l in Language.objects.all().order_by('pk')]), 'application/json')


@require_http_methods(['GET', 'POST'])
@csrf_protect
def login(request):
    from django.contrib.auth.views import login as auth_login
    from confucius.forms import AuthenticationForm

    return auth_login(request, authentication_form=AuthenticationForm)
