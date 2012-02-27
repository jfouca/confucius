from django.conf.urls.defaults import patterns, url

from confucius.views import ConferenceToggleView, ConferenceUpdateView, CreateAlertView, DashboardView, MembershipListView, EditAlert, DeleteAlert, SetDashboardView

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<pk>\d+)/set$', SetDashboardView.as_view(), name='dashboard_set'),
    url(r'^list/$', MembershipListView.as_view(), name='membership_list'),
    url(r'^(?P<pk>\d+)/update/$', ConferenceUpdateView.as_view(), name='conference_edit'),
    url(r'^(?P<pk>\d+)/toggle/$', ConferenceToggleView.as_view(), name='conference_toggle'),
    url(r'^(?P<pk>\d+)/alert/create/$', CreateAlertView.as_view(), name='create_alert'),
    url(r'^(?P<pk>\d+)/alert/(?P<alert_pk>\d+)/update$', EditAlert.as_view(), name='edit_alert'),
    url(r'^(?P<pk>\d+)/alert/(?P<alert_pk>\d+)/delete$', DeleteAlert.as_view(), name='delete_alert'),
)
