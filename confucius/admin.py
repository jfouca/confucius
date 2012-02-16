from django.contrib.admin import AdminSite, ModelAdmin, StackedInline
from confucius.models import Account, PostalAddress, EmailAddress, Language
from confucius.forms.authforms import AdminAccountForm


class EmailInline(StackedInline):
    #TO DO -> Should not be able to delete all email addresses ( must remain at least one ). idea : Verify Profile Model
    model = EmailAddress
    extra = 0


class PostalInline(StackedInline):
    model = PostalAddress
    extra = 0


class AccountAdmin(ModelAdmin):
    fields = ('first_name','last_name','languages')
    form = AdminAccountForm
    inlines = [EmailInline, PostalInline]


site = AdminSite()
site.register(Account, AccountAdmin)
