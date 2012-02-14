from django.contrib.admin import AdminSite, ModelAdmin , StackedInline, TabularInline
from confucius.models import User, Profile, Language


class ProfileInline(StackedInline) :
    model = Profile
    
class LanguageInline(StackedInline) :
    model = Language
    
class UserAdmin (ModelAdmin) :
    inlines = [ProfileInline]
    fields = ('last_name','first_name','username','password', 'is_active','last_login','date_joined','email', 'profile.secondary_email')
    #exclude = ('is_staff', 'is_superuser','groups','user_permissions')
    readonly_fields = ('last_login','date_joined')


class ProfileAdmin(ModelAdmin):
    inlines = [LanguageInline]


site = AdminSite ()
site.register(User,UserAdmin)
