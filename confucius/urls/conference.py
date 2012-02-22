from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from confucius.views import ConferenceUpdateView, MembershipListView

urlpatterns = patterns('confucius.views',
    url(r'^$', login_required(MembershipListView.as_view()), name='membership_list'),
    url(r'^update/(?P<pk>\d+)/$', login_required(ConferenceUpdateView.as_view()), name='conference_update'),
    #url(r'^/conf-create/$', 'create_conference', name='conf_create'),
    #url(r'^/conference/close/$', 'close_conference', name='close_conference'),
    #url(r'^/conference/open/$', 'open_conference', name='open_conference'),
)
