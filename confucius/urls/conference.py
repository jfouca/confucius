from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from confucius.models import Conference


urlpatterns = patterns('confucius.views',
    url(r'^$', ListView.as_view(model=Conference, template_name='conference/conference_list.html'), name='conferences'),
    #url(r'^/change/(?P<conf_id>\d+)/$', 'change_conference', name='change_conference'),
    #url(r'^/edit/$', 'edit_conference', name='edit_conference'),
    #url(r'^/home/$', 'home_conference', name='home_conference'),
    #url(r'^/conf-create/$', 'create_conference', name='conf_create'),
    #url(r'^/conference/close/$', 'close_conference', name='close_conference'),
    #url(r'^/conference/open/$', 'open_conference', name='open_conference'),
)
