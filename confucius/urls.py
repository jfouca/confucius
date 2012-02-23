from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import (login, logout,
        password_reset, password_reset_done, password_reset_confirm,
        password_reset_complete, password_change, password_change_done)
from django.contrib import admin 
from confucius.admin import site as admin
from confucius.views import close_account, edit_account, main_page, list_conference, edit_conference, create_conference, home_conference, change_conference, close_conference, open_conference, create_account, activate_account, invite_reviewer, reviewer_invitation_response

urlpatterns = patterns('',
    url(r'^$', main_page),
    url(r'^login/$', login, name='login'),
    url(r'^action/login/$', login,{'template_name':'registration/special_login.html'}, name='special_login'),
    url(r'^logged-out/$', logout, name='logout'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset-done/$',
        password_reset_done, name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset-complete/$',
        password_reset_complete, name='password_reset_complete'),
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change-done/$',
        password_change_done, name='password_change_done'),
    url(r'^account/$', edit_account, name='account'),
    url(r'^close-account/$', close_account, name='close_account'),
    url(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.urls)),
    url(r'^account-create/$', create_account, name='account-create'),
    url(r'^account-create/(?P<hashCode>.+)$', activate_account, name='account-activation'),
    url(r'^conferences/$', list_conference, name='conferences'),
    url(r'^conference/change/(?P<conf_id>\d+)$', change_conference, name='change_conference'),
    url(r'^conference/edit$', edit_conference, name='edit_conference'),
    url(r'^conference/home/$', home_conference, name='home_conference'),
    url(r'^conf-create/$', create_conference, name='conf_create'),
    url(r'^conference/close$', close_conference, name='close_conference'),
    url(r'^conference/open$', open_conference, name='open_conference'),
    url(r'^conference/reviewer$', invite_reviewer, name='reviewer'),
    url(r'^conference/reviewer/(?P<hashCode>.+)$', reviewer_invitation_response, name='reviewer_response'),
)
