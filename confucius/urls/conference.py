from django.conf.urls.defaults import patterns, include, url


basepatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^update/$', 'conference_edit', name='conference_edit'),
    url(r'^toggle/$', 'conference_toggle', name='conference_toggle'),
    (r'^alert/', include('confucius.urls.alert')),
    (r'^paper/', include('confucius.urls.paper')),
    (r'^review/', include('confucius.urls.review')),
)

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^list/$', 'membership_list', name='membership_list'),
    (r'^(?P<conference_pk>\d+)/', include(basepatterns)),
)
