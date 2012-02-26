from django.conf.urls.defaults import include, patterns
from django.conf import settings
from django.views.generic import RedirectView

from confucius import admin

urlpatterns = patterns('',
    (r'^$', RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL)),
    (r'^account/', include('confucius.urls.account')),
    (r'^conference/', include('confucius.urls.conference')),
    (r'^submission/', include('confucius.urls.submission')),
    (r'^admin/', include(admin.site.urls)),
)
