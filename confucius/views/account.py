from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.views.generic import DetailView

from confucius.forms import AddressFormSet, EmailFormSet, UserForm, UserCreationForm
from confucius.models import Activation, ActivationKey
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


from django.views.decorators.csrf import csrf_protect
@csrf_protect
def create_account(request, redirect_field_name='next'):
    next = request.REQUEST.get(redirect_field_name, '')
    
    if request.POST:
        form = UserCreationForm(request.POST)           
        if form.is_valid():
            created_user = form.save()
            #Penser a desactiver l'utilisateur

            import datetime
            expr_date = datetime.date.today() + datetime.timedelta(7)
            ActivationKey.objects.create(hash_code=created_user.username, user=created_user, expiration_date=expr_date, next_page=next)
            
            user_email = form.cleaned_data['email']
            send_mail('Confucius Account Creation', 'Please find enclose the activation link for your account : http://localhost:8000/account/create/'+created_user.username, 'no-reply@confucius.com',[user_email], fail_silently=False)
            
            return render_to_response('account/create_account_confirm.html', context_instance=RequestContext(request))
        else:
            return render_to_response('account/create_account.html',{"form":form,"next":next}, context_instance=RequestContext(request))
    
    #If no POST data, display an error (direct call)
    else:
        error_messages = "Account creation Unauthorized"
        return render_to_response('account/create_account.html',{"error_messages":error_messages}, context_instance=RequestContext(request))  


def activate_account(request, hashCode):
    assert hashCode is not None
    try:
        activationKey = ActivationKey.objects.get(hash_code=hashCode)
    except ActivationKey.DoesNotExist:
        return render_to_response('account/activate_account_confirm.html',
            {"error_message":"The provided Activation code is unknown"}, 
            context_instance=RequestContext(request))    
    
    #Check if the hashcode is still valid
    import datetime
    if datetime.date.today() > activationKey.expiration_date:
        return render_to_response('account/activate_account_confirm.html',
            {"error_message":"The provided Activation is expired"}, 
            context_instance=RequestContext(request))
    
    user = activationKey.user
    user.is_active=True
    user.save()
    activationKey.delete()
    
    #login user after activation
    from django.contrib.auth import login
    user.backend='django.contrib.auth.backends.ModelBackend' 
    login(request, user)
    
    return redirect(activationKey.next_page)
