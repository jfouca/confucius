from django.conf.urls.defaults import patterns, url
from confucius.views import auto_assignment

urlpatterns = patterns('confucius.views',
    url(r'^auto-assignment/(?P<pk_paper>\d+)$', 'auto_assignment'),
)
