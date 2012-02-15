from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import (login, logout,
        password_reset, password_reset_done, password_reset_confirm,
        password_reset_complete, password_change, password_change_done)

from confucius.views import edit_profile

urlpatterns = patterns('',
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
    url(r'^profile/$', edit_profile, name='profile')

)
