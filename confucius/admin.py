from django.contrib.admin import AdminSite, ModelAdmin, StackedInline

from confucius.models import Account, PostalAddress, EmailAddress, Conference
from confucius.forms.authforms import AdminAccountForm


class EmailInline(StackedInline):
    model = EmailAddress
    extra = 0


class PostalInline(StackedInline):
    model = PostalAddress
    extra = 0


class AccountAdmin(ModelAdmin):
    exclude = ('user',)
    form = AdminAccountForm
    inlines = [EmailInline, PostalInline]


site = AdminSite()
site.register(Account, AccountAdmin)
site.register(Conference)
