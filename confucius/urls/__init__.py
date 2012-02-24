from django.conf.urls.defaults import include, patterns

from confucius import admin

urlpatterns = patterns('',
    (r'^$', 'confucius.views.dashboard'),
    (r'^account/', include('confucius.urls.account')),
    (r'^conference/', include('confucius.urls.conference')),
    (r'^submission/', include('confucius.urls.submission')),
    (r'^admin/', include(admin.site.urls)),
)
