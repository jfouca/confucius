from django.conf.urls.defaults import patterns, url

# confucius views
urlpatterns = patterns('confucius.views',
    url(r'^$', 'account', name='account'),
    url(r'^languages/', 'languages', name='languages'),
    url(r'^confirm-email/(?P<activation_key>[0-9a-f]+)/$', 'confirm_email', name='confirm_email'),
    url(r'^password-change/$', 'password_change', name='password_change'),
    url(r'^close/$', 'close_account', name='close_account'),
)

# django.contrib.auth views
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^password-reset/$', 'password_reset', name='password_reset'),
    url(r'^password-reset-done/$', 'password_reset_done', name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', name='password_reset_confirm'),
    url(r'^password-reset-complete/$', 'password_reset_complete', name='password_reset_complete'),
)
