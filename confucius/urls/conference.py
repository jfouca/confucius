from django.conf.urls.defaults import patterns, url

from confucius.views import ConferenceToggleView, ConferenceUpdateView, MembershipListView

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^dashboard/(?P<conference_pk>\d+)/$', 'dashboard', name='dashboard'),
    url(r'^list/$', MembershipListView.as_view(), name='membership_list'),
    url(r'^update/(?P<pk>\d+)/$', ConferenceUpdateView.as_view(), name='conference_edit'),
    url(r'^toggle/(?P<pk>\d+)/$', ConferenceToggleView.as_view(), name='conference_toggle'),
    url(r'^mockuser/(?P<role_id>\d+)$', 'use_mockuser', name='mockuser_conference'),
    url(r'^exitmockuser/$', 'exit_mockuser', name='exit_mockuser_conference'),
    url(r'^create_alert$', 'create_alert', name='create_alert'),
)
