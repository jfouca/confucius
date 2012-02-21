from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import (login, logout,
        password_reset, password_reset_done, password_reset_confirm,
        password_reset_complete, password_change, password_change_done)

from confucius.admin import site as admin
from confucius.views import close_account, confirm_close_account, edit_account, main_page, list_conference, edit_conference, create_conference

urlpatterns = patterns('',
    url(r'^$', main_page),
    url(r'^login/$', login, name='login'),
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
    url(r'^closed-account/$', confirm_close_account, name='confirm_close_account'),
    url(r'^admin/', include(admin.urls)),
    url(r'^conferences/$', list_conference, name='conferences'),
    url(r'^conferences/(?P<conf_id>\d+)/$', edit_conference),
    url(r'^conf-create/$', create_conference),
)
