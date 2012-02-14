from django.conf.urls.defaults import patterns, include, url

from confucius.admin import site as admin_site
from confucius.views import login, profile

urlpatterns = patterns('',
    url(r'^login/', login),
    url(r'^profile/', profile),
    url(r'^admin/', include(admin_site.urls))
)
