from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

basepatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^papers/$', 'paper_list', name='papers'),
    url(r'^conference_papers/$', 'paper_list', {'get_all': True}, name='conference_papers'),
    url(r'^reviews/$', 'review_list', name='reviews'),
    url(r'^conference_reviews/$', 'review_list', {'get_all': True}, name='conference_reviews'),
    url(r'^alerts/$', 'alert_list', name='alerts'),
    url(r'^invitations/$', 'invitation_list', name='invitations'),
    url(r'^members/$', 'members_list', name='members_list'),
    url(r'^public/(?P<access_key>[0-9A-Za-z]{8})/$', 'conference_access', name='conference_access'),
    url(r'^membership/$', 'membership', name='membership'),
    url(r'^update/$', 'conference_edit', name='conference_edit'),
    url(r'^toggle/$', 'conference_toggle', name='conference_toggle'),
    url(r'^invite/$', 'conference_invite', name='conference_invite'),
    url(r'^send-email-to-users/$', 'send_email_to_users', name='send_email_to_users'),
    (r'^alert/', include('confucius.urls.alert')),
    (r'^paper/', include('confucius.urls.paper')),
    (r'^review/', include('confucius.urls.review')),
)

urlpatterns = patterns('confucius.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^list/$', 'membership_list', name='membership_list'),
    url(r'^invitation/(?P<key>[0-9a-f]{64})/$', 'conference_invitation', name='conference_invitation'),
    url(r'^invitation/(?P<key>[0-9a-f]{64})/(?P<decision>accept|refuse)/$', 'conference_invitation', name='conference_invitation'),
    url(r'^refusal/$', TemplateView.as_view(template_name='conference/refusal.html'), name='refusal'),
    url(r'^already-answered/$', TemplateView.as_view(template_name='conference/already_answered.html'), name='already_answered'),
    url(r'^signup/(?P<key>[0-9a-f]{64})/$', 'signup', name='signup'),
    (r'^(?P<conference_pk>\d+)/', include(basepatterns)),
)
