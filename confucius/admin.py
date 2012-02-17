from django.contrib.admin import AdminSite, ModelAdmin, StackedInline
from confucius.models import Account, PostalAddress, EmailAddress, Language, Conference, Role, ConferenceAccountRole
from confucius.forms.authforms import AdminAccountForm


class EmailInline(StackedInline):
    #TO DO -> Should not be able to delete all email addresses ( must remain at least one ). idea : Verify Profile Model
    model = EmailAddress
    extra = 1


class PostalInline(StackedInline):
    model = PostalAddress
    extra = 1
    

class AccountRoleConfInLine(StackedInline):
    model = ConferenceAccountRole
    can_add = ('account',)
    extra = 1

class AccountAdmin(ModelAdmin):
    fields = ('first_name','last_name','languages')
    form = AdminAccountForm
    inlines = [EmailInline, PostalInline]

class ConferenceAdmin(ModelAdmin):
    inlines = [AccountRoleConfInLine]

site = AdminSite()
site.register(Account, AccountAdmin)
site.register(Conference, ConferenceAdmin)
