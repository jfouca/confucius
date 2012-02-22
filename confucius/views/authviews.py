import datetime
from django import forms
from django.db import IntegrityError
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from confucius.forms import CreateAccountForm
from django.forms.models import modelform_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.mail import send_mail
from confucius.models import Account, EmailAddress, PostalAddress, AccountManager, ActivationKey


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

    if request.method == 'POST':
        request.user.is_active = False
        request.user.save()
        logout(request)
        return HttpResponseRedirect(reverse('confirm_close_account'))
    return render_to_response('account/close_account.html', context_instance=RequestContext(request))


def confirm_close_account(request):
    return render_to_response('account/confirm_close_account.html', context_instance=RequestContext(request))


def create_account(request):
        
    if request.POST:
        form = CreateAccountForm(request.POST)        
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password_1 = form.cleaned_data.get("password_1", "")
            password_2 = form.cleaned_data["password_2"]
            if password_1 != password_2 :
                form.error_messages = form.error_messages['password_mismatch']
                return render_to_response('account/create_account.html',{"form":form}, context_instance=RequestContext(request))
            
            #basic account creation
            account_mngr = AccountManager()
            try:
                account = account_mngr.create(email=email, password=password_1, last_name=last_name, is_active=False)
            except IntegrityError:
                form.error_messages = form.error_messages['duplicate_username']
                return render_to_response('account/create_account.html',{"form":form}, context_instance=RequestContext(request))
            
            print account.user.username
            
            #Adding first_name
            account.user.first_name = first_name
            account.user.save()
            
            expr_date = datetime.date.today() + datetime.timedelta(7)
            ActivationKey.objects.create(hash_code=account.user.username, linked_account=account, expiration_date=expr_date)
            
            send_mail('Confucius Account Creation', 'Please find enclose the activation link for your account : http://localhost:8000/account-create/'+account.user.username, 'no-reply@confucius.com',[email], fail_silently=False)
            
            return render_to_response('account/create_account_confirm.html', context_instance=RequestContext(request))            
            
            #Authenticate and login user after creation
            #user = authenticate(username=email, password=password_1)
            #login(request, user)
            #return redirect('/account/')
                              
    else:
        form = CreateAccountForm()
        form.error_messages = None
    
    return render_to_response('account/create_account.html',{"form":form}, context_instance=RequestContext(request))    


def activate_account(request, hashCode):
    
    assert hashCode is not None
    try:
        activationKey = ActivationKey.objects.get(hash_code=hashCode)
    except ActivationKey.DoesNotExist:
        return render_to_response('account/activate_account_confirm.html',
            {"error_message":"The provided Activation code is unknown"}, 
            context_instance=RequestContext(request))
    
    #Check if the hashcode exist
    #if activationKey == None :
         
    
    #Check if the hashcode is still valid
    if datetime.date.today() > activationKey.expiration_date:
        return render_to_response('account/activate_account_confirm.html',
            {"error_message":"The provided Activation is expired"}, 
            context_instance=RequestContext(request))
    
    account = activationKey.linked_account
    account.user.is_active=True
    account.user.save()
    
    activationKey.delete()
    
    #login user after activation
    account.user.backend='django.contrib.auth.backends.ModelBackend' 
    login(request, account.user)
    
    return render_to_response('account/activate_account_confirm.html', context_instance=RequestContext(request))
    
    
