from django.contrib.admin import AdminSite, ModelAdmin, StackedInline

from confucius.models import Account, PostalAddress, EmailAddress, Language, Conference, Role, ConferenceAccountRole, Alert, Domain, Reminder, Event, Action
from confucius.forms.authforms import AdminAccountForm, ConferenceAccountRoleForm
from django.forms.widgets import CheckboxSelectMultiple


class EmailInline(StackedInline):
    model = EmailAddress
    extra = 0


class PostalInline(StackedInline):
    model = PostalAddress
    extra = 0


class AccountRoleConfInLine(StackedInline):
    model = ConferenceAccountRole
    extra = 0
    form = ConferenceAccountRoleForm


class AccountAdmin(ModelAdmin):
    exclude = ('user',)
    form = AdminAccountForm
    inlines = [EmailInline, PostalInline]


class ConferenceAdmin(ModelAdmin):
    inlines = [AccountRoleConfInLine]

site = AdminSite()
site.register(Account, AccountAdmin)
site.register(Conference, ConferenceAdmin)
site.register(Domain)
