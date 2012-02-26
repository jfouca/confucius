from django.conf.urls.defaults import patterns, url
from confucius.views import auto_assignment, submit_review

urlpatterns = patterns('confucius.views',
    url(r'^auto-assignment/(?P<pk_paper>\d+)$', 'auto_assignment'),
    url(r'^submit/(?P<pk_assignment>\d+)$', 'submit_review', name="submit_review"),
)
