from django.conf.urls.defaults import patterns, include, url


basepatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^update/$', 'conference_edit', name='conference_edit'),
    url(r'^toggle/$', 'conference_toggle', name='conference_toggle'),
    url(r'^invite/$', 'conference_invite', name='conference_invite'),
    url(r'^invitation/(?P<key>[0-9a-f]+)/accept$', 'conference_invitation', name='invitation_accept'),
    url(r'^invitation/(?P<key>[0-9a-f]+)/refuse$', 'conference_invitation', name='invitation_refuse'),
    (r'^alert/', include('confucius.urls.alert')),
    (r'^paper/', include('confucius.urls.paper')),
    (r'^review/', include('confucius.urls.review')),
)

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^list/$', 'membership_list', name='membership_list'),
    (r'^(?P<conference_pk>\d+)/', include(basepatterns)),
)
