from django.conf.urls.defaults import patterns, url

from confucius.views import ConferenceToggleView, ConferenceUpdateView, MembershipListView, EditAlert

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^dashboard/(?P<conference_pk>\d+)/$', 'dashboard', name='dashboard'),
    url(r'^list/$', MembershipListView.as_view(), name='membership_list'),
    url(r'^update/(?P<pk>\d+)/$', ConferenceUpdateView.as_view(), name='conference_edit'),
    url(r'^toggle/(?P<pk>\d+)/$', ConferenceToggleView.as_view(), name='conference_toggle'),
    url(r'^create_alert/(?P<conference_pk>\d+)$', 'create_alert', name='create_alert'),
    url(r'^edit_alert/(?P<pk>\d+)/$', EditAlert.as_view(), name='edit_alert'),
)
