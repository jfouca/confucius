from django.contrib.admin import AdminSite
from confucius.models import User, Profile, Language

site = AdminSite ()

site.register(User)
site.register(Profile)
site.register(Language)

