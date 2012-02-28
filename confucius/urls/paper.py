from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('confucius.views',
    url(r'^submit$', 'paper', name='paper'),
    url(r'^(?P<paper_pk>\d+)/update/$', 'paper', name='paper'),
)
