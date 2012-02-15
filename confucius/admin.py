from django.contrib.admin import AdminSite, ModelAdmin , StackedInline
from confucius.models import User, Profile, Language


class ProfileInline(StackedInline) :
    model = Profile
    can_delete = False
    
class LanguageInline(StackedInline) :
    model = Language
    
class UserAdmin (ModelAdmin) :
    inlines = [ProfileInline]
    exclude = ('is_staff', 'is_superuser','groups','user_permissions')
    readonly_fields = ('last_login','date_joined')


class ProfileAdmin(ModelAdmin):
    inlines = [LanguageInline]


site = AdminSite ()
site.register(User,UserAdmin)
