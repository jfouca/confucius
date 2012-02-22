from django.contrib.admin import AdminSite, ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from confucius.forms import AddressFormSet, EmailFormSet, UserCreationForm, UserForm, ConferenceUserRoleForm
from confucius.models import Address, Email, Conference, ConferenceUserRole, Domain


class AdminUserForm(UserForm):
    class Meta(UserForm.Meta):
        fields = ('email', 'first_name', 'is_active', 'is_superuser', 'last_name')


class AddressInline(StackedInline):
    extra = 0
    formset = AddressFormSet
    model = Address


class EmailInline(StackedInline):
    extra = 0
    formset = EmailFormSet
    model = Email


class UserAdmin(AuthUserAdmin):
    actions = ['activate', 'deactivate']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {
            'fields': ('is_active', 'password')
        }),
        ('Personal information', {
            'fields': (('first_name', 'last_name'),)
        }),
        ('Languages', {
            'classes': ('collapse',),
            'fields': ('languages',)
        })
    )
    filter_horizontal = ()
    form = AdminUserForm
    inlines = [AddressInline, EmailInline]
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_superuser')
    list_display_links = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_superuser', 'date_joined')
    ordering = ()
    readonly_fields = ('password', )
    search_fields = ('email', 'first_name', 'last_name')

    def queryset(self, request):
        return User.objects.filter(pk=request.user.pk)

    def update_is_active(self, request, queryset, is_active):
        rows_updated = queryset.update(is_active=is_active)

        if rows_updated == 1:
            message_bit = '1 user was'
        else:
            message_bit = '%s users were' % rows_updated

        self.message_user(request, "%s successfully %s." % (message_bit, 'activated' if is_active else 'deactivated'))

    def activate(self, request, queryset):
        self.update_is_active(request, queryset, True)

    def deactivate(self, request, queryset):
        self.update_is_active(request, queryset, False)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs.update({'form': UserCreationForm})

        return super(UserAdmin, self).get_form(request, obj, **kwargs)

    def get_formsets(self, request, obj=None, **kwargs):
        for inline in self.inline_instances:
            if obj is None:
                continue
            yield inline.get_formset(request, obj)


class UserRoleConfInLine(StackedInline):
    model = ConferenceUserRole
    extra = 0
    form = ConferenceUserRoleForm


class ConferenceAdmin(ModelAdmin):
    inlines = [UserRoleConfInLine]

site = AdminSite()
site.register(User, UserAdmin)
site.register(Conference, ConferenceAdmin)
site.register(Domain)
