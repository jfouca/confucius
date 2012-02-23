from django.conf.urls.defaults import patterns, url

from confucius.views import ConferenceToggleView, ConferenceUpdateView, MembershipListView

urlpatterns = patterns('confucius.views',
    url(r'^$', MembershipListView.as_view(), name='membership_list'),
    url(r'^update/(?P<pk>\d+)/$', ConferenceUpdateView.as_view(), name='conference_update'),
    url(r'^toggle/(?P<pk>\d+)/$', ConferenceToggleView.as_view(), name='conference_toggle'),
    url(r'^conference/mockuser/(?P<role_id>\d+)$', 'use_mockuser', name='mockuser_conference'),
    url(r'^conference/exitmockuser/$', 'exit_mockuser', name='exit_mockuser_conference'),
)
