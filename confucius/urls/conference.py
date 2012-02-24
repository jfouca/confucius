from django.conf.urls.defaults import patterns, url

from confucius.views import ConferenceToggleView, ConferenceUpdateView, MembershipListView

urlpatterns = patterns('confucius.views',
    url(r'^$', MembershipListView.as_view(), name='membership_list'),
    url(r'^update/(?P<pk>\d+)/$', ConferenceUpdateView.as_view(), name='conference_update'),
    url(r'^toggle/(?P<pk>\d+)/$', ConferenceToggleView.as_view(), name='conference_toggle'),
    url(r'^mockuser/(?P<role_id>\d+)$', 'use_mockuser', name='mockuser_conference'),
    url(r'^exitmockuser/$', 'exit_mockuser', name='exit_mockuser_conference'),
    url(r'^create_alert$', 'create_alert', name='create_alert'),
    url(r'^reviewer_invitation$', 'reviewer_invitation', name='reviewer_invitation'),
    url(r'^reviewer_invitation/(?P<hashCode>.+)$', 'reviewer_response', name='reviewer_response'),
)
