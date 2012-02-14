from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from confucius.admin import site as admin_site
from confucius.views import login, profile

urlpatterns = patterns('',
    url(r'^login/', login),
    url(r'^profile/', profile),
    url(r'^admin/', include(admin_site.urls)),
    url(r'^passreset/$',auth_views.password_reset,name='forgot_password1'),
    url(r'^passresetdone/$',auth_views.password_reset_done,name='forgot_password2'),
    url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='forgot_password3'),
    url(r'^passresetcomplete/$',auth_views.password_reset_complete,name='forgot_password4'),
)