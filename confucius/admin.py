from django.contrib.admin import AdminSite, ModelAdmin , StackedInline
from confucius.models import User, Profile, Language


class ProfileInline(StackedInline) :
    model = Profile
    
class UserAdmin (ModelAdmin) :
    inlines = [ ProfileInline ]


site = AdminSite ()
site.register(User,UserAdmin)
site.register(Language)

