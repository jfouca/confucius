from django.conf.urls.defaults import patterns, url
from confucius.views import auto_assignment, submit_review, paper_selection_list, read_reviews

urlpatterns = patterns('confucius.views',
    url(r'^auto-assignment/(?P<pk_paper>\d+)$', 'auto_assignment'),
    url(r'^submit/(?P<pk_assignment>\d+)$', 'submit_review', name="submit_review"),
    url(r'^selection/$', 'paper_selection_list', name="paper_selection_list"),
    url(r'^read/(?P<pk_paper>\d+)$', 'read_reviews', name="read_reviews"),
    url(r'^finalize/$', 'finalize_selection', name="finalize_selection"),
    url(r'^assignments/$', 'assignments', name="assignments"),
)
