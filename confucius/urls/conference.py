from django.conf.urls.defaults import patterns, url

from confucius.views import ConferenceToggleView, ConferenceUpdateView, CreateAlertView, DashboardView, MembershipListView, EditAlert, DeleteAlert

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<pk>\d+)/$', DashboardView.as_view(), name='dashboard'),
    url(r'^list/$', MembershipListView.as_view(), name='membership_list'),
    url(r'^update/(?P<pk>\d+)/$', ConferenceUpdateView.as_view(), name='conference_edit'),
    url(r'^toggle/(?P<pk>\d+)/$', ConferenceToggleView.as_view(), name='conference_toggle'),
    url(r'^create-alert/(?P<pk>\d+)$', CreateAlertView.as_view(), name='create_alert'),
    url(r'^edit_alert/(?P<pk>\d+)/$', EditAlert.as_view(), name='edit_alert'),
    url(r'^delete_alert/(?P<pk>\d+)/$', DeleteAlert.as_view(), name='delete_alert'),
)
