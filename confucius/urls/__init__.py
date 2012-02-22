from django.conf.urls.defaults import include, patterns

from confucius import admin

urlpatterns = patterns('',
    (r'^account/', include('confucius.urls.account')),
    (r'^admin/', include(admin.site.urls)),
)
