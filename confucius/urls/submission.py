from django.conf.urls.defaults import patterns, url
from confucius.views import submit_paper
urlpatterns = patterns('confucius.views',
    url(r'^submit-paper/(?P<pk_conference>\d+)/$', 'submit_paper', name='submit_paper'),
    url(r'^edit-paper/(?P<pk_conference>\d+)/(?P<pk_paper>\d+)$', 'submit_paper', name='edit_paper'),
)
