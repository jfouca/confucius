from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('confucius.views',
    url(r'^create$', 'alert', name='alert'),
    url(r'^(?P<alert_pk>\d+)/update$', 'alert', name='alert'),
    url(r'^(?P<alert_pk>\d+)/delete$', 'delete_alert', name='delete_alert'),
)
