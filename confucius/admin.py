from django.contrib.admin import AdminSite, ModelAdmin , StackedInline
from confucius.models import Profile, Language, PostalAddress, EmailAddress

class EmailInline(StackedInline):

#TO DO -> Should not be able to delete all email addresses ( must remain at least one ). idea : Verify Profile Model
    model = EmailAddress
    extra = 0

class PostalInline(StackedInline):
    model = PostalAddress
    extra = 0
    
class ProfileAdmin(ModelAdmin):
    exclude = ('user',)
    inlines = [EmailInline, PostalInline]

site = AdminSite ()
site.register(Profile, ProfileAdmin)
