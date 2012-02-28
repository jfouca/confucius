from django.conf.urls.defaults import patterns, include, url


basepatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^public/(?P<access_key>[0-9A-Za-z]{8})/$', 'conference_access', name='conference_access'),
    url(r'^membership/$', 'membership', name='membership'),
    url(r'^update/$', 'conference_edit', name='conference_edit'),
    url(r'^toggle/$', 'conference_toggle', name='conference_toggle'),
    url(r'^invite/$', 'conference_invite', name='conference_invite'),
    url(r'^invitation/(?P<key>[0-9a-f]{128})/accept$', 'conference_invitation', name='invitation_accept'),
    url(r'^invitation/(?P<key>[0-9a-f]{128})/refuse$', 'conference_invitation', name='invitation_refuse'),
    (r'^alert/', include('confucius.urls.alert')),
    (r'^paper/', include('confucius.urls.paper')),
    (r'^review/', include('confucius.urls.review')),
)

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^list/$', 'membership_list', name='membership_list'),
    (r'^(?P<conference_pk>\d+)/', include(basepatterns)),
)
