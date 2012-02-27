from django.conf.urls.defaults import patterns, url
from confucius.views import CreatePaperView

urlpatterns = patterns('confucius.views',
    url(r'^(?P<pk>\d+)/submit-paper/$', CreatePaperView.as_view(), name='submit_paper'),
    url(r'^edit-paper/(?P<pk>\d+)/(?P<pk_paper>\d+)$', 'submit_paper', name='edit_paper'),
)
